from setuptools import setup, find_packages
with open("readme.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

from djmicroservice import __version__ 
setup(
    name='djmicroservice',
    description='django micro service app.',
    version='1.0.7',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tangdyy/djmicroservice",    
    author='Tang dayong',
    author_email='674822668@qq.com',
    packages=find_packages(),
    requires=['django', 'djangorestframework'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'     
)
