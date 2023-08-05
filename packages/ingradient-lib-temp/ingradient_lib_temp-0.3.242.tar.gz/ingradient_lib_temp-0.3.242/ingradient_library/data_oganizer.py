from ingradient_library.preprocessing import Cropping
import SimpleITK as sitk
import pickle
import os
import numpy as np
from ingradient_library.preprocessing import Resampling
import torch

class Data_Organizer(object):
    # Resampling 후 저장 추가해야 됨.
    def __init__(self, SAVE_PATH, ID = 'ingradient', resampling = None, normalizer = None):
        self.crop = Cropping()
        self.SAVE_PATH = SAVE_PATH
        self.ID = ID
        self.resampling = resampling
        self.normalizer = normalizer
    
    def set_direction(self, img, direction):
        direction = np.array(direction).reshape(3,3)
        inverse = np.where(direction == -1)[0]
        permute = np.where(direction != 0)[1]
        if 0 in inverse:
            img = img[::-1, :, :]

        if 1 in inverse:
            img = img[:, ::-1, :]

        if 2 in inverse:
            img = img[:, :, ::-1]

    def run(self, seg_path, img_path_list, index, modality = ['CT']):
        seg = sitk.ReadImage(seg_path)
        save_dict = dict()
        if self.resampling != None:
            save_dict['target_spacing'] = self.resampling.target_spacing
        save_dict['spacing'] = seg.GetSpacing()
        save_dict['direction'] = seg.GetDirection()
        save_dict['origin'] = seg.GetOrigin()
        save_dict['modality'] = modality
        seg = sitk.GetArrayFromImage(seg)
        save_path = os.path.join(self.SAVE_PATH, self.ID+str(index)+'_info.pkl')
        pickle_file = open(save_path, 'wb')
        pickle.dump(save_dict, pickle_file)
        pickle_file.close()

        for i in range(len(img_path_list)):
            img_path = img_path_list[i]
            img = sitk.ReadImage(img_path)
            img = sitk.GetArrayFromImage(img)
            if len(img.shape) != 4:
                img = np.expand_dims(img, axis = 0)
            if i == 0:
                images = img
            else:
                images = np.vstack(images, img)
        
        for i in range(len(images)):
            images[i] = self.set_direction(images[i], save_dict['direction'])
            
            if not self.mode == 'train' :
                seg = self.set_direction(seg, save_dict['direction'])

        img_arr, seg_arr = self.crop(images, seg)

        if self.normalizer != None:
            img_arr = self.normalizer(img_arr)

        

        if self.resample != None:
            y = torch.tensor(seg_arr.copy())
            x = torch.tensor(img_arr.copy())
            if self.mode == 'train' :
                result = self.resample(torch.vstack((x, y.unsqueeze(0))), save_dict)
                x = result[:-1]
                y = result[-1].squeeze(0)
            
            else:
                x = self.resample(x, save_dict)
        
        np.savez(os.path.join(self.SAVE_PATH, self.ID+str(index)+'.npz'), x =img_arr.numpy(), y=seg_arr.numpy())

    