import numpy as np
from PIL import Image
from scipy.ndimage import zoom
from matplotlib import pyplot as plt
import pandas as pd
from glob import glob
from pathlib import Path
import os
from tqdm import tqdm


class AsciiTable:
    def __init__(self, alphabet, img_type, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.alphabet = alphabet
        self.img_type = img_type
        self.image_df = self.image_df()
        self.print_table()

    def image_df(self):
        df = pd.DataFrame(columns=["dimension", "img_path", "label", "format"])
        if self.img_type == "png":
            for i, img_path in enumerate(glob(self.input_path + "/*.png")):
                df.loc[i, "dimension"] = plt.imread(img_path).shape
                df.loc[i, "img_path"] = img_path
                df.loc[i, "label"] = os.path.basename(img_path).split(".")[0]
                df.loc[i, "format"] = os.path.basename(img_path).split(".")[1]
        elif self.img_type == "jpg":
            for i, img_path in enumerate(glob(self.input_path + "/*.jpg")):
                df.loc[i, "dimension"] = plt.imread(img_path).shape
                df.loc[i, "img_path"] = img_path
                df.loc[i, "label"] = os.path.basename(img_path).split(".")[0]
                df.loc[i, "format"] = os.path.basename(img_path).split(".")[1]
        else:
            pass #TODO this logic needs to be improved
        return df

    def generate_images(self):
        chars = self.alphabet.chars
        v = 60*3 #TODO change the parameters in the function call instead of hardcoded here
        h = 100*3
        sr = 0
        df = self.image_df

        print("Begin image generation")
        for i, rows in tqdm(df.iterrows(),total=df.shape[0], desc="Images generated:"):
            img_path = df.loc[i, "img_path"]
            img = AsciiImage(img_path,
                             chars,
                             vert=v,
                             horiz=h,
                             simp_rate=sr)
            df.loc[i, "image"] = img.characteriser()

    def print_table(self):#, folder_name):
        #TODO catch if image not yet generated
        location = self.output_path#f'C:/Users/Andrew/PycharmProjects/ASCII_Art/Output/{folder_name}'
        Path(location).mkdir(parents=True, exist_ok=True)
        output = self.image_df
        #output.to_csv(self.folder_path + "/table.csv") #TODO make this work smarter with filepaths
        output.to_csv(location + "/___table.csv")

    def print_images(self):#, folder_name):
        # TODO maybe this is best to write each image during the generation steps?
        #TODO catch if image not yet generated
        #location = f'C:/Users/Andrew/PycharmProjects/ASCII_Art/Output/{folder_name}'
        location = self.output_path#f'C:/Users/Andrew/PycharmProjects/ASCII_Art/Output/{folder_name}'
        labels = self.image_df['label']
        images = self.image_df['image']
        Path(location).mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(images):
            with open(f"{location}/{labels[i]}.txt", "w") as t:
                t.write(img)


class AsciiImage:

    def __init__(self, filepath, characters, vert, horiz, simp_rate=None):
        self.filepath = filepath
        self.characters = characters
        self.vert = vert
        self.horiz = horiz
        self.label = filepath[filepath.rfind('/') + 1:filepath.rfind('.')]
        self.image = np.asarray(Image.open(filepath).convert('L')) # TODO why is this happening?
        self.simp_rate = simp_rate
        self.ascii_image = self.characteriser()

    def characteriser(self):
        # apply simplification and coercion to image
        coerced_img = self.coerce_image(self.image, self.vert, self.horiz)
        simplified_img = self.simplify_image(coerced_img, self.simp_rate)
        # then loop through each image and characterise them
        img_list = simplified_img.tolist()
        output = []
        for row in img_list:
            characterised_row = []
            # here, each row is an array of numbers (from 0 - 255)
            for number in row:
                # lookup the number val against Alphabet dict, replace in that position
                character = self.characters[number]
                characterised_row.append(character)
            output.append("".join(characterised_row))
        return "\n".join(output)

    def print_output(self, alt_destination=None):
        # write an individual ascii image to a text file
        if alt_destination is None:
            with open("Output/Output.txt", "w") as text_file:
                text_file.write(self.ascii_image)
        else:
            with open(alt_destination + "Output/_Output.txt", "w") as text_file:
                text_file.write(self.ascii_image)
        print("Output printed.")

    @staticmethod
    def coerce_image(image, x_size, y_size):
        # force the image to be a fixed resolution by interpolating the npy array to user specified size
        x_shape, y_shape = image.shape
        x_zoom, y_zoom = x_size / x_shape, y_size / y_shape
        return zoom(image, [x_zoom, y_zoom])

    @staticmethod
    def simplify_image(image, simp_rate):
        # round numbers in each ndarray to reduce character count, simulates decreasing resolution
        return np.floor_divide(image, int(2 ** (8 * simp_rate))) * int(2 ** (8 * simp_rate))
