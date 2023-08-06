from torch.utils.tensorboard import SummaryWriter
import torch.optim as optim
from torch.utils.data import random_split
import torch
import time
from ingradient_library.dataloads import *
from ingradient_library.model import *
from ingradient_library.preprocessing import *
from ingradient_library.deep_supervision_loss import *
from ingradient_library.visualization import *
from ingradient_library.optimizer import SAMSGD
from ingradient_library.sampling import *


class Trainer(object):
    def __init__(self, tr_dataloader, model,  optimizer, scheduler, losses, regulizers = [], is_deep_supervision = False,
                deep_supervision_weight = 0.5, n_epoch = 1000, val_dataloader = None, save_path = None):
 
        self.model = model
        self.optimizer = optimizer
        self.n_epoch = n_epoch
        self.save_path = save_path
        self.visualization = None
        self.tr_dl = tr_dataloader
        self.val_dl = val_dataloader
        self.scheduler = scheduler
        self.losses = losses
        self.is_deep_supervision = is_deep_supervision
        self.deep_supervision_weight = deep_supervision_weight
        self.regulizers  = regulizers
        if len(self.regulizers) == 0:
            self.regulizers = [1] * len(self.losses)
            
    def calculate_loss(self, output, target, writer, epoch):
        if self.is_deep_supervision == True:
            batch_size = output.shape[0]
            deep_supervision_size = output.shape[1]
            channel_size = output.shape[2]
            output = output.reshape(batch_size * deep_supervision_size, channel_size, -1)
            target = target.reshape(batch_size, 1, -1).repeat(1, deep_supervision_size,1).reshape(batch_size * deep_supervision_size, -1)
            weight = torch.ones(deep_supervision_size).to(output.device.index)
            weight.requires_grad = False
            acc_value = self.deep_supervision_weight
            for i in range(deep_supervision_size):
                weight[i] = acc_value ** i
            
            weight = weight / weight.sum()
            weight = weight.view(1,deep_supervision_size ,1)
        
        else:
            batch_size = output.shape[0]
            channel_size = output.shape[1]
            output = output.reshape(batch_size, channel_size, -1)
            target = target.reshape(batch_size, -1)

        for i in range(len(self.losses)):
            loss = self.losses[i]
            temp = loss(output, target) * torch.tensor(self.regulizers[i]).to(output.device.index)
            for _ in range(len(temp.shape)-1):
                temp = temp.mean(-1)
            writer.add_scalar('Iteration\Loss_'+ str(type(loss)), temp[0], epoch)
            if self.is_deep_supervision == True:
                temp = temp.view(batch_size, deep_supervision_size, -1)
            if i == 0:
                losses = temp
            else:
                losses += temp

        
        if self.is_deep_supervision == True:
            result = (losses * weight).mean()
            
        else:
            result = losses.mean()

        return result
    


    def load_model_state_dict(self, path, load_classifier = False):
        pretrained_dict = torch.load(path)
        if not load_classifier:
            classifier = list(self.model._modules)[-1]
            for k in list(pretrained_dict.keys()):
                if classifier in k:
                    del pretrained_dict[k]

        current_dict = self.backbone.state_dict()
        current_dict.update(pretrained_dict)
        self.backbone.load_state_dict(current_dict)

    def run(self):
        writer = SummaryWriter()
        for e in range(self.n_epoch):
            self.tr_dl.new_epoch()
            n_iter = 0
            self.model.train()
            
            while not self.tr_dl.is_end():
                n_iter += 1
                images, seg = self.tr_dl.generate_train_batch()
                if isinstance(self.optimizer, SAMSGD):
                    def closure():
                        self.optimizer.zero_grad()
                        output = self.model(images)
                        loss = self.calculate_loss(output, seg, writer, e)
                        loss.backward()
                        return loss
                    self.optimizer.step(closure)
                
                else:
                    output = self.model(images)
                    self.optimizer.zero_grad()
                    loss = self.calculate_loss(output, seg, writer, e)
                    if self.tr_dl.current_index == 0:
                        deep_supervision_visualization(output, seg)
                    loss.backward()
                    self.optimizer.step()


            if self.val_dl != None:
                self.val_dl.new_epoch()
                val_loss = 0
                n_iter = 0
                self.model.eval()
                while not self.val_dl.is_end():
                    n_iter +=1
                    with torch.no_grad():
                        images, seg = self.val_dl.generate_train_batch()
                        output = self.model(images)
                        loss = self.calculate_loss(output, seg, writer, e)
                        if self.visualization != None:
                            if self.val_dl.current_index == 0:
                                self.visualization(output, seg)
                
            self.scheduler.step()
            if self.save_path != None:
                file_name = 'epoch'+ str(e) + '_model_state_dict.pkl'
                torch.save(self.model.state_dict(), os.path.join(self.save_path, file_name))
        


class Interactive_Trainer(Trainer):
    def __init__(self, tr_dataloader, model, optimizer, scheduler, losses, regulizers=[], is_deep_supervision=False, deep_supervision_weight=0.5, n_epoch=1000, val_dataloader=None, save_path=None, n_point = 10 ):
        super().__init__(tr_dataloader, model, optimizer, scheduler, losses, regulizers=regulizers, is_deep_supervision=is_deep_supervision, deep_supervision_weight=deep_supervision_weight, n_epoch=n_epoch, val_dataloader=val_dataloader, save_path=save_path)
        self.n_point = 10

    def calculate_loss(self, output, target, writer, epoch):
        return super().calculate_loss(output, target, writer, epoch)
    
    def run(self, visualization_ineterval = 5, summary_writer_path = None):
        if summary_writer_path != None:
            writer = SummaryWriter(summary_writer_path)
        else:
            writer = SummaryWriter()
        for e in range(self.n_epoch):
            self.tr_dl.new_epoch()
            train_loss = 0
            n_iter = 0
            self.model.train()
            
            while not self.tr_dl.is_end():
                n_iter += 1
                images, seg = self.tr_dl.generate_train_batch()
                bs, _, nx, ny, nz = images.shape #bs, n_modalities, 
                #First
                positive_points, negative_points = point_sampler(seg, first = True)
                output = self.model(images, positive_points, negative_points)
                self.optimizer.zero_grad()
                loss = self.calculate_loss(output, seg, writer, e)
                train_loss = loss.item()
                
                center = output.shape[3] // 2
                if self.tr_dl.current_index % visualization_ineterval == 0:
                    print("points : ", 0)
                    visualization(output, seg)
                loss.backward()
                self.optimizer.step()

                for i in range(self.n_point):
                    zero_grad = time.time()
                    self.optimizer.zero_grad()
                    print('zero grad', time.time() - zero_grad)
                    prev_seg_time = time.time()
                    prev_seg = output.detach()
                    print('prev_seg', time.time()- prev_seg_time)
                    ps_time = time.time()
                    point_sampler(seg, prev_seg, positive_points, negative_points)
                    out_time = time.time()
                    print('ps time', time.time()- ps_time)
                    output = self.model(images, positive_points, negative_points, prev_seg)
                    loss_time = time.time()
                    print('out time', time.time()- out_time)
                    loss = self.calculate_loss(output, seg, writer, e)
                    train_loss = loss.item()
                    if self.tr_dl.current_index % visualization_ineterval == 0:
                        print("points : ",i + 1)
                        visualization(output, seg)
                    loss.backward()
                    self.optimizer.step()
                    print('out time', time.time()- loss_time)
            self.scheduler.step()


            if self.save_path != None:
                file_name = 'epoch'+ str(e) + '_model_state_dict.pkl'
                torch.save(self.model.state_dict(), os.path.join(self.save_path, file_name))
