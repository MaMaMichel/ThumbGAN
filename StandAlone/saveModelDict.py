import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib 
import matplotlib.pyplot as plt
import torch
import pickle
import re

class GeneratorDeconv(torch.nn.Module):
    """"""
    def __init__(self):
        super().__init__()
        self.compression = torch.nn.Sequential(
            #torch.nn.Conv2d(1, 5, (5,3),stride=(6,1), padding=(0,1)),
            torch.nn.Linear(1920,192),
            torch.nn.BatchNorm1d(192),
            torch.nn.ReLU())
        
        self.deconv0 = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(1, 128, 3, stride = 2, padding=2),
            torch.nn.BatchNorm2d(128,32,32),
            torch.nn.ReLU())
        
        self.deconv1 = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(128, 64, 4, stride = 2, padding=0),
            torch.nn.BatchNorm2d(64,32,32),
            torch.nn.ReLU())
        
        self.deconv2 = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(64, 32, 4, stride=2, padding=[0,1]),
            torch.nn.BatchNorm2d(32,90,120),
            torch.nn.ReLU())
        
        self.out = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(32, 3, 7, stride = 1, padding=3),
            torch.nn.BatchNorm2d(3,90,120),
            torch.nn.Sigmoid())

    def forward(self, x):
        #x = self.compression(x.reshape(batch_size,1,30,64))
        x = self.compression(x.reshape(batch_size,1920))
        x = self.deconv0(x.reshape(batch_size,1,12,16))
        x = self.deconv1(x)
        x = self.deconv2(x)
        x = self.out(x)
        return x

generator = torch.load('./generator_cat3_50000')

torch.save(generator.state_dict(), 'state_dict_cat3_50000')