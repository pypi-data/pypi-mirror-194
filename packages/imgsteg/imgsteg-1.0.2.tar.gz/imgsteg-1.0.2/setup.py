from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name = 'imgsteg',
    packages = ['imgsteg'],
    version = '1.0.2',
    license = 'MTL',
    description = 'python library for image steganography. used to encrypt and decrypt text message inside an image',
    long_description=long_description,
    long_description_content_type='text/markdown',
    authon = 'Mohammed Sujaid',
    author_email = 'sujaidsujaid1162@gmail.com',
    url = 'https://sujaid.pythonanywhere.com',
    keywords = ['image steganography', 'steganography', 'image', 'sujaid'],
    install_requires = [
        'numpy',
        'Pillow'
    ],
    requires_python = ">=3.8",
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    ]
)