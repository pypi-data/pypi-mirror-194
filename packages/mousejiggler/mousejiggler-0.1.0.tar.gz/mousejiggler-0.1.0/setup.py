from setuptools import setup, find_packages

setup(
    name='mousejiggler',
    version='0.1.0',
    description='A package to keep your cat AND screensaver busy.',
    author='Idriss CHEBAK',
    author_email='idrisschebak@me.com',
    packages=find_packages(),
    install_requires=[
        'Pillow',
    ],
)
