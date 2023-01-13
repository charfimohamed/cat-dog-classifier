import logging
import os
import sys
from pathlib import Path

#import hydra
import torch
import torch.nn as nn
import wandb
from torch.optim import Adam
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from src.data import make_dataset
from src.data.make_dataset import CatDogDataset
from src.models.train_model import *

#sys.path.append("..")
#log = logging.getLogger(__name__)
#print = log.info


#training_function
def test (batch_size = 32):
    ''' tests the neural network after training'''
    #print("_____")
    #DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.load('model_best_checkpoint.pth')
    model=CatDogModel()
    checkpoint = torch.load('model_best_checkpoint.pth')
    model.load_state_dict(checkpoint['model'])
    model.eval()
    #model.to(DEVICE)
    
    image_size = model.im_size
    data_resize = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])])

    test_dataset = CatDogDataset(split="test", in_folder=Path("../../data/raw"), out_folder=Path('../../data/processed'), transform=data_resize)
    test_dataloader = DataLoader(test_dataset, batch_size = batch_size, shuffle=True)
    nb_test_samples=0
    test_accuracy = 0
    for i,(images, labels) in enumerate(test_dataloader) :
        print(f"test step {i}")
        outputs = model(images)
        _, preds = torch.max(outputs, dim=1)
        test_accuracy+=torch.sum(preds==labels)
        nb_test_samples += preds.shape[0]
    test_accuracy = test_accuracy /nb_test_samples
    print(f"test accuracy : {test_accuracy}")
    

        #wandb.log({
            #'epoch': epoch, 
            #'train_acc': train_acc,
            #'train_loss': train_loss, 
            #'val_acc': val_acc, 
            #'val_loss': val_loss
        #})

        #print('Average loss for epoch : {i}'.format(i=total_loss/len(train_loader)))
    
    return model  

if __name__ == "__main__":
    test()