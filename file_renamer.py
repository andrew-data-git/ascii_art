import os
from glob import glob
import re


# fixes the autosort by alphabetical into numerical
def numerical_sort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# run the replacing algorithm
input_path = "C:/Users/Andrew/PycharmProjects/ASCII_Art/images/hobbit"
for index, file in enumerate(sorted(glob(f'{input_path}/*.jpg'), key=numerical_sort)):
    # pad the index by 9
    padded = str(index).rjust(9, "0")
    os.rename(os.path.join(input_path, file), os.path.join(input_path, '_hobbit'.join([str(padded), '.jpg'])))
