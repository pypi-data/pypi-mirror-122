from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pixqrcode',
    version='1.0.0',
    packages=['src'],
    url='',
    license='',
    author='Joao Carlos',
    author_email='joao-mostela@hotmail.com',
    description='QRCode Pix for python',
    python_requires=">=3.6"
)
