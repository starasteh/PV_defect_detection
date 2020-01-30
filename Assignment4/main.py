'''
This is the main function running the Training, Validation, Testing process.
Set the hyper-parameters and model parameters here. [data parameters from config file]
@author: Soroosh Tayebi Arasteh <soroosh.arasteh@fau.de>
'''

# Deep Learning Modules
from torch.nn import *
import torch
import torch.optim as optim

# User Defined Modules
from configs.serde import *
from Train_Test_Valid import *
from models.resnet import *
from stopping import EarlyStoppingCallback
from data.data import *

#System Modules
from itertools import product
import numpy as np
from matplotlib import pyplot as plt

import warnings
warnings.filterwarnings('ignore')




def main_train():
    '''Main function for training + validation'''

    '''Hyper-parameters'''
    NUM_EPOCH = 15
    LOSS_FUNCTION = CrossEntropyLoss  #Todo
    OPTIMIZER = optim.Adam
    parameters = dict(lr = [.01], batch_size = [1])
    param_values = [v for v in parameters.values()]

    '''Hyper-parameter testing'''
    for lr, BATCH_SIZE in product(*param_values):
        # put the new experiment name here.
        params = create_experiment("Adam_lr" + str(lr) +'_batch_size'+ str(BATCH_SIZE))
        cfg_path = params["cfg_path"]

        '''Prepare data'''
        # Train Set
        full_train_dataset = ChallengeDataset(cfg_path=cfg_path, split_ratio=0.8, mode=Mode.TRAIN)
        train_size = int(0.8 * len(full_train_dataset))
        valid_size = len(full_train_dataset) - train_size
        train_dataset, valid_dataset = torch.utils.data.random_split(full_train_dataset, [train_size, valid_size])

        train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE,
                                                   drop_last=True, shuffle=True, num_workers=4)
        valid_loader = torch.utils.data.DataLoader(dataset=valid_dataset, batch_size=BATCH_SIZE,
                                                   drop_last=True, shuffle=True, num_workers=4)
        '''Initialize trainer'''
        trainer = Training(cfg_path)
        '''Define model parameters'''
        optimiser_params = {'lr': lr}
        MODEL = resnet(vocab_size=VOCAB_SIZE, batch_size=BATCH_SIZE)
        trainer.setup_model(model=MODEL, optimiser=OPTIMIZER,
                            optimiser_params=optimiser_params, loss_function=LOSS_FUNCTION, weight_ratio=)
        '''Execute Training'''
        trainer.execute_training(train_loader, valid_loader=valid_loader, num_epochs=NUM_EPOCH)



# initialize the early stopping callback implemented in stopping.py and create a object of type Trainer


def main_test():
    '''Main function for prediction'''
    pass



def experiment_deleter():
    '''Use below lines if you want to delete an experiment and reuse the same experiment name'''
    parameters = dict(lr = [.01], batch_size = [32])
    param_values = [v for v in parameters.values()]
    for lr, BATCH_SIZE in product(*param_values):
        delete_experiment("Adam_" + str(lr) +'_batch_size'+ str(BATCH_SIZE))



if __name__ == '__main__':
    # experiment_deleter()
    main_train()
    # main_test()
