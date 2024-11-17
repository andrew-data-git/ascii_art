from ascii_image import AsciiImage
from alphabet import Alphabet

from PIL import Image
from pathlib import Path
from tqdm import tqdm
import os
import glob


class AsciiGif:
    def __init__(self, path_to_gif: str, n_frames: int = None):
        self.gif = Image.open(Path(path_to_gif))
        if n_frames == None:
            self.n_frames = self.gif.n_frames
        else:
            self.n_frames = n_frames
        self.ascii_frames = list()

    def convert(self, alphabet, simp_rate: float, cell_size: int):
        '''For a frame, convert it into a ascii_frame'''
        # Clear /frames directory
        files = glob.glob('frames/*')
        for f in files:
            os.remove(f)

        # Loop through frames and write into /frames directory
        for i, frame in enumerate(tqdm(range(self.n_frames-1), desc="Converting frames")):
            # Move to the current frame
            self.gif.seek(frame) 
            # Process and save
            ascii_frame = AsciiImage(alphabet=alphabet, 
                               frame=self.gif.copy(),
                               simp_rate=simp_rate,
                               cell_size=cell_size)    
            ascii_frame.ascii_image.save(Path(f'frames/frame_{i}.gif'))

    def save(self, path: str):
        '''Save the asciifed frames as a new gif'''
        # Read the contents of /frames and append to self.ascii_frames
        for i in range(self.n_frames-1):
            self.ascii_frames.append(
                Image.open(Path(f'frames/frame_{i}.gif'))
                )

        # Convert to a new gif and save
        self.ascii_frames[0].save(Path(path),
                            save_all=True, 
                            append_images=self.ascii_frames[1:],
                            loop=0) # indefinite loop

if __name__ == '__main__':
    print('Initiate conversion.')
    ascii_gif = AsciiGif('river.gif')
    ascii_gif.convert(alphabet=Alphabet(25),
                      simp_rate=0.25, 
                      cell_size=5)
    print('Conversion complete.')
    ascii_gif.save('ascii_gif.gif')
    print('Saved.')