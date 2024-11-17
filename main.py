from ascii_image import AsciiImage
from alphabet import Alphabet

from PIL import Image
from pathlib import Path

class AsciiGif:
    def __init__(self, path_to_gif: str):
        self.ascii_frames = []
        self.gif = Image.open(Path(path_to_gif))
        self.n_frames = self.gif.n_frames

    def convert(self, alphabet, simp_rate):
        '''For a frame, convert it into a ascii_frame'''
        for i, frame in enumerate(range(self.n_frames-1)):
            self.gif.seek(frame)  # Move to the current frame
            frame_copy = self.gif.copy()  # Copy the frame to manipulate if needed
            ascii = AsciiImage(alphabet=alphabet, 
                               frame=frame_copy,
                               simp_rate=simp_rate)
            if i%10 == 0:
                print(f'Converted frame {i+1} of {self.n_frames}')            
            self.ascii_frames.append(ascii.ascii_image)

    def save(self):
        '''Save the asciifed frames as a new gif'''
        self.ascii_frames[0].save('ascii_gif.gif',
                            save_all=True, 
                            append_images=self.ascii_frames[1:],#[self.ascii_gif.copy() for _ in range(self.n_frames-1)], 
                            loop=0) # indefinite loop

if __name__ == '__main__':
    print('Initiate conversion.')
    ascii_gif = AsciiGif('river.gif') 
    ascii_gif.convert(Alphabet(25), 0.25)
    print('Conversion complete.')
    ascii_gif.save()
    print('Saved.')