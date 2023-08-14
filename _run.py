import random
import ascii
import alphabet

random.seed = 1
full_alphabet = alphabet.Alphabet(25)

table = ascii.AsciiTable(input_path="C:/Users/Andrew/PycharmProjects/ASCII_Art/images/hobbit",
                         output_path="C:/Users/Andrew/PycharmProjects/ASCII_Art/Output/hobbit",
                         alphabet=full_alphabet,
                         img_type="jpg")
table.generate_images()
table.print_images()
