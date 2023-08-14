from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from tqdm import tqdm
import glob
import os


class AsciiImage:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.text_to_image(font_size=6, image_size=(1280, 1280))

    def text_to_image(self, font_size, image_size):
        # TODO this should inherit from the AsciiTable thing
        # set up params, including a white background rectangle
        image = Image.new('RGB', image_size, color=(255, 255, 255))
        with open(self.input_file, 'r') as file:
            text_content = file.read()
        # draw the image, and add the text, while identifying text content dimensions to be centralised
        font_location = 'C:/Users/Andrew/PycharmProjects/ASCII_Art/venv/Lib/site-packages/matplotlib/mpl-data/fonts'
        font = ImageFont.truetype(font=font_location+"/FiraMono-Medium.otf", size=font_size)
        draw = ImageDraw.Draw(image)
        w_, h_ = image_size
        _, _, w, h = draw.textbbox((0, 0), text_content, font=font)
        draw.text(((w_-w)/2, (h_-h)/2), text_content, fill=(0, 0, 0), font=font, align="center", )
        #image.save(self.output_file)
        self.image = image

    def save(self):
        # prints the image
        self.image.save(self.output_file)

def run_on_all_images(input_folder, output_folder):
    df = pd.read_csv(input_folder + "/___table.csv")
    labels = df["label"]
    for label in tqdm(labels):
        input_file = input_folder+"/"+label+".txt"
        output_file = output_folder+"/"+label+".png"
        result = AsciiImage(input_file, output_file)
        result.save()

if __name__ == "__main__":
    # run_on_all_images(input_folder="C:/Users\Andrew\PycharmProjects\ASCII_Art\Output/hobbit",
    #                   output_folder="C:/Users\Andrew\PycharmProjects\ASCII_Art\Output/hobbit_png")

    # Create the frames
    frames = []

    path1 = "C:/Users\Andrew\PycharmProjects\ASCII_Art\Output/hobbit_png"
    for frame in os.listdir(path1):
        new_frame = Image.open(path1 + "/" + frame)
        frames.append(new_frame)
    
    # Save into a GIF file
    path2 = "C:/Users\Andrew\PycharmProjects\ASCII_Art\Output"
    frames[0].save(path2 + "/../output/animation.gif", format='GIF',
                   append_images=frames[60:140],
                   save_all=True,
                   duration=41, loop=1, transparency=1)

