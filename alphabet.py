import random

class Alphabet:
    """
    A class to generate an Alphabet, for use in generating ASCII images.

    Attributes:
        alphabet : str
            A default alphabet, ranging from 'dark' to 'light' characters
    Methods:
        update_alphabet(chars)
            Updates the default alphabet if user required
        create()
            Forms the Alphabet object based on user input, and matches in a dict with number 0 -> 255 for lookups
    """
    alphabet = "#@%$8WMXHQ35420/xzoes+=~-"

    def __init__(self, size, chars=None):
        """
        Parameters
        :param size:
        :param chars:
        """
        self.size = size
        if chars is None:
            self.raw = None
            print("Using base alphabet.")
        else:
            self.raw = chars
            self.update_alphabet(chars)
        self.chars = self.create()

    def __len__(self):
        """Returns the length of the alphabet string before/after processing"""
        print("Length of raw alphabet = 25")
        len(self.chars) # TODO make this actually work

    def update_alphabet(self, chars):
        """Updates the default alphabet if user required"""
        # remove duplicates and set as alphabet
        self.alphabet = "".join(dict.fromkeys(chars))

    def create(self):
        """Forms the Alphabet object based on user input, and matches in a dict with number 0 -> 255 for lookups"""
        # pick the chars from alphabet
        try:
            indices = sorted(random.sample(range(len(self.alphabet)), self.size))
        except:
            raise ValueError("Too large. Requested size exceeds total length of unique characters.")
        chars = ''.join(self.alphabet[index] for index in indices)

        colour_count = int(255 / self.size)
        colour_chars = "".join([char * colour_count for char in chars])

        # catch missing characters, replace with last character
        if len(colour_chars) < 256:
            colour_chars = colour_chars + colour_chars[-1] * (256 - len(colour_chars))

        # form into dictionary
        print(f"Character set of size {self.size} characters created from input: {self.raw}.")
        print(f"Alphabet = {chars}")
        return dict(enumerate(colour_chars))
