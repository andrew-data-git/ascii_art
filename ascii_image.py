import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
import matplotlib as mpl
import matplotlib.pyplot as plt


class AsciiImage:
    '''Class to hold an ascii representation of an image'''
    def __init__(self, alphabet:dict, frame=None, simp_rate=0.1):
        if frame==None: # capture raw greyscale image
            print('No path specified! Defaulting to Gollum.')
            self.raw_image = Image.open(Path('gollum.png')).convert('L')
        else:
            self.raw_image = frame.convert('L')#Image.open(Path('gollum.png')).convert('L')
        self._coerce_image(simp_rate) # make self.simple_image
        self.alphabet = alphabet
        self._convert_to_ascii_image() # make self.ascii_image

    def _coerce_image(self, simp_rate):
        '''Decreasing image resolution, maintain original size.'''
        width, height = self.raw_image.size
        w2, h2 = math.floor(width*simp_rate), math.floor(height*simp_rate)
        self.image = self.raw_image.resize((w2,h2), Image.Resampling.LANCZOS) # downsample
        # self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)# upscale

    def _convert_to_ascii_image(self):
        '''Take the processed self.image and convert into ascii.'''
        map_func = np.vectorize(self.alphabet.chars.get)
        self._np_array = np.asarray(self.image) # store the np array if needed
        self._ascii_array = map_func(self._np_array) # store the ascii array if needed

        # Make blank canvas
        cell_size = 20
        w, h = self.image.size
        canvas = Image.new(mode="RGB", 
                           size=(w*cell_size, h*cell_size), 
                           color="white")
        draw = ImageDraw.Draw(canvas)
        
        # Set font
        font = ImageFont.truetype("cmtt10.ttf", cell_size*1.25)
        
        # Draw each character on the image
        for i, row in enumerate(self._ascii_array):
            for j, char in enumerate(row):
                x = j*cell_size
                y = i*cell_size
                draw.text((x, y), char, fill="black", font=font)
        self.ascii_image =  canvas # store the array as PIL image

    def plot(self):
        '''For the image, show the three states of it's conversion side by side.'''
        mpl.use('TkAgg')
        fig, (ax0,ax1,ax2) = plt.subplots(nrows=1, ncols=3, figsize=(6,12))
        ax0.imshow(self.raw_image)
        ax1.imshow(self.image)
        ax2.imshow(self.ascii_image)
        fig.suptitle('Raw, Processed and ASCII images')
        plt.show()
