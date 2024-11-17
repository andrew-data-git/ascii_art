import random


class Alphabet:
    """A class to generate an Alphabet, for use in generating ASCII images."""
    def __init__(self, size: int) -> None:
        self.alphabet = "#@%$8WMXHQ35420/xzoes+=~-"
        self.size = size
        self.create() # Make the self.chars attribute

    def __len__(self):
        len(self.chars)

    def create(self):
        """Forms the Alphabet object based on user input, and matches in a dict with number 0 -> 255 for lookups"""
        # Pick the chars from alphabet
        random.seed(1)
        try:
            indices = sorted(random.sample(range(len(self.alphabet)), self.size))
        except:
            raise ValueError(f"Choose another size for alphabet. Size = {self.size} > {len(self.alphabet)}")
        
        colour_count = int(255 / self.size)
        colour_chars = "".join([char * colour_count for char in ''.join(self.alphabet[index] for index in indices)])

        # Catch missing characters, replace with last character
        if len(colour_chars) < 256:
            colour_chars = colour_chars + colour_chars[-1] * (256 - len(colour_chars))
        self.chars = dict(enumerate(colour_chars))
