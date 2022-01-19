import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from easygui import msgbox
import PySimpleGUI as sg
import matplotlib 
import matplotlib.pyplot as plt
import torch
import pickle
import re

batch_size = 64

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

'''
class GeneratorDeconv(torch.nn.Module):
    """"""
    def __init__(self):
        super().__init__()
        self.compression = torch.nn.Sequential(
            #torch.nn.Conv2d(1, 5, (5,3),stride=(6,1), padding=(0,1)),
            torch.nn.Linear(1920,1600),
            torch.nn.BatchNorm1d(1600),
            torch.nn.ReLU())
        
        self.linear1 = torch.nn.Sequential(
            torch.nn.Linear(1600,1280),
            torch.nn.BatchNorm1d(1280),
            torch.nn.ReLU())
        
        self.deconv1 = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(5, 5, 4, stride = 2, padding=1),
            torch.nn.BatchNorm2d(5,32,32),
            torch.nn.ReLU())
        
        self.deconv2 = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(5, 3, (3, 4), stride=(3,4), padding=(3, 4)),
            torch.nn.BatchNorm2d(3,90,120),
            torch.nn.ReLU())
        
        self.out = torch.nn.Sequential(
            torch.nn.ConvTranspose2d(3, 3, 7, stride = 1, padding=3),
            torch.nn.BatchNorm2d(3,90,120),
            torch.nn.Sigmoid())

    def forward(self, x):
 
        #x = self.compression(x.reshape(batch_size,1,30,64))
        x = self.compression(x.reshape(batch_size,1920))
        x = self.linear1(x)
        x = self.deconv1(x.reshape(batch_size,5,16,16))
        x = self.deconv2(x)
        x = self.out(x)
        return x
'''


lookUpDict = pickle.load(open( "./lookUpDict25.pickle", "rb" ))


#generator = torch.load('./generator_cat_144000')
generator = GeneratorDeconv()
generator.load_state_dict(torch.load('./state_dict_cat3_50000'))


## Cant put model in eval mode bacuse batch normalization layer would return NaN

#generator.eval()



def string_to_vector(input_string, lookUp):
    
    output = []
    
    for word in input_string.split(' '):
        output.append(list(lookUp[word]))
        
    return output



matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Define the window layout
layout = [
    [sg.Text("ThumbGen v0.1")],
    [sg.Text("Please enter up to 25 words separated by spaces:")],
    [sg.InputText()],
    [sg.Button("Generate!")],
    [sg.Canvas(key="-CANVAS-")],
    [sg.Button("CLOSE")],
]

# Create the form and show it without the plot
window = sg.Window(
    "ThumbGen v0.1",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)



while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'CLOSE': # if user closes window or clicks cancel
        break
    elif event == 'Generate!':

        if values[0] != '':

            input_noise = torch.rand(batch_size, 320)

            input_string = re.sub('[^a-zA-Z0-9 ]', '', values[0].lower())

            try:

                input_vector = np.array(string_to_vector(input_string, lookUpDict)).flatten()

                input_vector =np.pad(input_vector, (0, 25*64*batch_size - input_vector.size), mode='constant', constant_values=0)
            
                input_vector = torch.from_numpy(input_vector).reshape(batch_size,1600)

                print(input_vector.size())

                sample = torch.cat((input_vector, input_noise), 1)

                sample = sample#.cuda()


                output = generator(sample)

                output = output.reshape(batch_size,3,90,120)
                output = output.split([1,batch_size-1])[0]
                output = output.reshape(3,90,120)
         

                output = output.detach()

                output = output.numpy()


                output = output.transpose((1,2,0))

                fig = matplotlib.figure.Figure(figsize=(4, 3), dpi=100)
                fig.add_subplot(111).imshow(output)

                draw_figure(window["-CANVAS-"].TKCanvas, fig)

            except:

                msgbox('Word not in vocabulary...', 'Error', 'Ok...')

            


#window.close()

#japanese symbol for beginner excel red heart smiling cat with heart eyes red heart 4



