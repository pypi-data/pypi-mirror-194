"""
    - This python librarie is for image steganography.
    - Its contains two method called Encrypt and Decrypt.

# package use example
>>pip3 install imgsteg

# How encryption work

>>import imgsteg as stg
>>obj = imgsteg
>>image = "name and path of the image including extension"  #image = "car.png"
>>new_image = "new.png"
>>message = "your message that want to encrypt"
>>obj.Encrypt(image, message, new_image)

# How decryption work

>>import imgsteg as stg
>>obj = imgsteg
>>image = "name and path of the image including extension"  #image = "car.png"
>>data = obj.Decrypt(image)
>>print(data.message)
"""
import numpy as ny
from PIL import Image


class Encrypt:
    """
    # How encryption work
    >>import imgsteg as stg
    >>obj = imgsteg
    >>image = "name and path of the image including extension"  #image = "car.png"
    >>new_image = "new.png"
    >>message = "your message that want to encrypt"
    >>obj.Encrypt(image, message, new_image)
    """

    def __init__(self, image, plain_text, new_file):
        print("Please wait it takes some time")
        try:
            self.file1 = Image.open(image)
        except FileNotFoundError:
            self.file_error(image)
            return None
        self.file = ny.array(self.file1.convert('RGB'), dtype=ny.uint8)
        self.plain_text = plain_text
        self.new_file = new_file
        self.data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                     'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23,
                     'x': 24, 'y': 25, 'z': 26, '1': 27, '2': 28, '3': 29, '4': 30, '5': 31, '6': 32, '7': 33, '8': 34,
                     '9': 35, '0': 36, 'a0': 37, '!': 38, '@': 39, '#': 40, '$': 41, '%': 42, '^': 43, '&': 44, '*': 45,
                     '(': 46, ')': 47, '-': 48, '_': 49, '+': 50, '=': 51, '~': 52, '[': 53, ']': 54, '{': 55, '}': 56,
                     ':': 57, ';': 58, '.': 59, ',': 60, '?': 61, '/': 62, '\'': 63, '\\': 64, 'A': 65, 'B': 66,
                     'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77,
                     'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88,
                     'Y': 89, 'Z': 90}
        self.print_output()

    def file_error(self, image):
        print(f"No such file or directory called {image}")

    def print_output(self):
        self.adding_data()
        img = Image.fromarray(self.file, 'RGB')
        img.save(self.new_file)

    def ascci_code(self):
        if self.plain_text:
            ad = str(self.plain_text[0:1])
            if ad == ' ':
                ad = 'a0'
            self.plain_text = self.plain_text[1:]
            return self.data.get(ad)
        return "done"

    def adding_data(self):
        for i in range(len(self.file)):
            for j in range(len(self.file[2])):
                for k in range(len(self.file[2, 2])):
                    if i == j == 0 and k == 2:
                        self.file[i, j, 2] = int(len(self.plain_text))

                    else:
                        if k == 2:
                            new = self.file[i, j, k]
                            if new == 0:
                                ad = self.ascci_code()
                                if ad == "done":
                                    return
                                else:
                                    self.file[i, j, k] += ad
                            else:
                                ad = self.ascci_code()
                                if ad == "done":
                                    return
                                else:
                                    self.file[i, j, k] = ad


class Decrypt:
    """
    # How decryption work

    >>import imgsteg as stg
    >>obj = imgsteg
    >>image = "name and path of the image including extension"  #image = "car.png"
    >>data = obj.Decrypt(image)
    >>print(data.message)
    """

    def __init__(self, image):
        try:
            self.file1 = Image.open(image)
        except FileNotFoundError:
            self.file_error(image)
            return None
        self.file = ny.array(self.file1.convert('RGB'), dtype=ny.uint8)
        self.list = []
        self.mes = ''
        self.data = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 10, 'k': 11, 'l': 12,
                     'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19, 't': 20, 'u': 21, 'v': 22, 'w': 23,
                     'x': 24, 'y': 25, 'z': 26, '1': 27, '2': 28, '3': 29, '4': 30, '5': 31, '6': 32, '7': 33, '8': 34,
                     '9': 35, '0': 36, 'a0': 37, '!': 38, '@': 39, '#': 40, '$': 41, '%': 42, '^': 43, '&': 44, '*': 45,
                     '(': 46, ')': 47, '-': 48, '_': 49, '+': 50, '=': 51, '~': 52, '[': 53, ']': 54, '{': 55, '}': 56,
                     ':': 57, ';': 58, '.': 59, ',': 60, '?': 61, '/': 62, '\'': 63, '\\': 64, 'A': 65, 'B': 66,
                     'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77,
                     'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88,
                     'Y': 89, 'Z': 90}
        self.message = self.get_output()

    def file_error(self, image):
        print(f"No such file or directory called {image}")

    def getting_length(self):
        return self.file[0, 0, 2]

    def get_list(self):
        ln = self.getting_length()
        z = 0
        for i in range(len(self.file)):
            for j in range(len(self.file[2])):
                for k in range(len(self.file[2, 2])):
                    if i == j == 0 and k == 2:
                        continue
                    if k == 2:
                        if z >= ln:
                            return "The file dont have any encrypted text"
                        m = self.file[i, j, 2]
                        if m >= 91:
                            return "The file don't have any encrypted text"
                        self.list.append(m)
                        z += 1

    def get_data(self):
        self.get_list()
        for i in self.list:
            m = list(self.data.keys())[list(self.data.values()).index(i)]
            if m == 'a0':
                self.mes += ' '
            else:
                self.mes += m

    def get_output(self):
        self.get_data()
        return self.mes
