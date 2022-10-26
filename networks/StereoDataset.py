import torch.utils.data
import os
import skimage.io as io
from torch.utils.data import Dataset
import numpy as np


class StereoDataset(Dataset):
    def __init__(self, hparams, transform=None):
        super().__init__()
        self.data_path = hparams['data_path']
        self.left_input_path = os.path.join(self.data_path,'low_light/low_left')
        self.right_input_path = os.path.join(self.data_path, 'low_light/low_right')
        self.gt_path = os.path.join(self.data_path, 'high_light/high_depth')
        self.transform = transform
        # maybe add quality later

    def __len__(self):
        return len(os.listdir(*[self.input_path]))

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        left_input_name = os.path.join(self.left_input_path, 'image_'+str(idx+1)+'.png')
        left_input = io.imread(left_input_name)
        left_input = np.divide(left_input, 255) #normalize image to be in [0,1]

        right_input_name = os.path.join(self.right_input_path, 'image_' + str(idx + 1) + '.png')
        right_input = io.imread(right_input_name)
        right_input = np.divide(right_input, 255)  # normalize image to be in [0,1]

        gt_name = os.path.join(self.gt_path, 'image_'+str(idx+1)+'.png')
        gt = io.imread(gt_name)
        gt = np.divide(gt, 255) #normalize image to be in [0,1]

        sample = {'left_input': left_input, 'right_input': right_input, 'gt': gt}

        if self.transform:
            sample = self.transform(sample)

        return sample