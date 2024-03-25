'''
Author: meetai meetai@gmx.com
Date: 2024-03-25 12:12:00
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-25 12:44:14
FilePath: /IJCAI15-srccode/ds.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import torch
from torch.utils.data import Dataset
from PIL import Image
import pytorch_lightning as pl


def image_transformer(image):
    return torch.ones(32),100
class CustomDataset(Dataset):
    def __init__(self, data_paths, labels, transform=image_transformer):
        self.data_paths = data_paths  # 数据文件的路径列表
        self.labels = labels  # 对应的标签列表
        self.transform = transform  # 可选的转换操作

    def __len__(self):
        import os
        entries = os.listdir(self.data_paths)
        #return len(entries)
        return 100

    def __getitem__(self, idx):
        return torch.ones(32),100
        # 加载数据
  #      image = Image.open(self.data_paths[idx]).convert('RGB')
  #      # 获取标签
  #      label = self.labels[idx]
  #      # 应用转换（如果有的话）
  #      if self.transform:
  #          image = self.transform(image)
  #      # 返回数据和标签
  #      return image, label

## 假设你有一些数据路径和对应的标签
#data_paths = ['path/to/image1.jpg', 'path/to/image2.jpg', ...]
#labels = [0, 1, ...]  # 例如，0代表类别1，1代表类别2
#
## 创建数据集实例
#dataset = CustomDataset(data_paths, labels)
#
## 可以使用 PyTorch 的 DataLoader 来迭代数据集
#from torch.utils.data import DataLoader
#
#data_loader = DataLoader(dataset, batch_size=32, shuffle=True)

## 现在可以迭代数据加载器来获取批次数据
#for images, labels in data_loader:
#    # 在这里执行训练步骤
#    pass

from torch.utils.data import DataLoader

class MyDataModule(pl.LightningModule):
    def __init__(self, data_paths="data", labels=[], batch_size=32):
        super().__init__()
        self.data_paths = data_paths
        self.labels = labels
        self.batch_size = batch_size

    def setup(self, stage=None):
        # 创建数据集实例
        self.dataset = CustomDataset(self.data_paths, self.labels)
        # 创建 DataLoader 实例
        self.dataloader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        print(self.dataloader)

    def train_dataloader(self):
        # 返回训练数据加载器
        return self.dataloader

    def val_dataloader(self):
        # 如果有验证集，返回验证数据加载器
        # 这里可以返回另一个 DataLoader 实例
        return self.dataloader

    def test_dataloader(self):
        # 如果有测试集，返回测试数据加载器
        # 这里可以返回另一个 DataLoader 实例
        return self.dataloader