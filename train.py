'''
Author: meetai meetai@gmx.com
Date: 2024-03-25 11:58:54
LastEditors: meetai meetai@gmx.com
LastEditTime: 2024-03-25 12:52:34
FilePath: /IJCAI15-srccode/train.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''


from torch import nn
from torch.optim import Adam
import pytorch_lightning as pl



class HandwritingModelEval(pl.LightningModule):
    def __init__(self):
        super(HandwritingModelEval, self).__init__()
        self.l1 = nn.Linear(32,256)
        self.ac1 = nn.ReLU()
        self.l2 = nn.Linear(256,10)
        self.ac2 = nn.ReLU()
        self.l3 = nn.Linear(10,1)
        self.ac3 = nn.ReLU()
        self.criterion = nn.MSELoss()

    def forward(self, x):
        return self.ac3(self.l3(self.ac2(self.l2(self.ac1(self.l1(x))))))

    def training_step(self, batch, batch_idx):
        inputs,labels = batch #torch.tensor(batch) 
        outputs = self(torch.tensor(inputs))
        loss = self.criterion(torch.tensor(labels).float(),outputs)
        return loss

    def validation_step(self, batch, batch_idx):
        pass

    def test_step(self, batch, batch_idx):
        pass

    def configure_optimizers(self):
                # 定义优化器
        optimizer = Adam(self.parameters(), lr=1e-4)
        # 如果需要，可以添加学习率调度器
        scheduler = {
            'scheduler': torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9),
            'name': 'steplr',
            'interval': 'epoch',
            'frequency': 1
        }
        return [optimizer], [scheduler]
        


if __name__=="__main__":
    print("main")
    from pytorch_lightning.callbacks.early_stopping import EarlyStopping
    from pytorch_lightning.callbacks import ModelCheckpoint
    from copy import deepcopy
    import torch
    import gc

    model = HandwritingModelEval()
    # trainer config
    trainer = pl.Trainer(
        max_epochs=10,
        callbacks=[
            EarlyStopping(monitor='dev_loss',patience=2), # 監測dev_loss的變化，超過兩次沒有改進就停止
            ModelCheckpoint(monitor='dev_loss',filename='{epoch}-{dev_loss:.2f}',save_last=True),
        ]
    )

    # DataModule
    from ds import *
    dm = MyDataModule()

    # train
    # 使用tuner自動尋找最佳batch_size
    # 目前已知在1.2.7會有點小問題
    # 使用deepcopy來避免trainer參數跑掉
    #tuner = pl.tuner.tuning.Tuner(deepcopy(trainer))
    #new_batch_size = tuner.scale_batch_size(model, datamodule=dm, init_val=torch.cuda.device_count())
    #del tuner
    #gc.collect()
    # 將找到的batch_size指定過去
    #model.hparams.batch_size = new_batch_size
    trainer.fit(model,datamodule=dm)