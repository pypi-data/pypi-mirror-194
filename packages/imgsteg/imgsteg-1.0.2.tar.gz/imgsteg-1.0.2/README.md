This is a python library for image steganography. Using this library user can encrypt and decrypt text message inside an image.

# How to use this package

# need to install package

>>pip install imgsteg

In .py file

>>import imgsteg

create object

>>obj = imgsteg

How encryption work

>>image = "name and path of the image including extension"  #image = "car.png"
>>new_image = "new.png"
>>message = "your message that want to encrypt"
>>obj.Encrypt(image, message, new_image)

How decryption work

>>image = "name and path of the image including extension"  #image = "car.png"
>>data = obj.Decrypt(image)
>>print(data.message)
