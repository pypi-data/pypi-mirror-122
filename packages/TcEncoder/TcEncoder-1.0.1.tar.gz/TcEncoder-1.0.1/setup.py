from setuptools import setup

setup(
    name = 'TcEncoder',
    version = '1.0.1',
    author = 'Maycon Guimarães',
    author_email = 'maycon.vnc@gmail.com',
    packages = ['TcEncoder'],
    description='It is a function to encode and decode easier string,list and dictionarys using a password in Python',
    keywords = 'encoder and decoder using only a password',
    install_requires=["cryptography==3.4.7"]
)