from setuptools import setup, find_packages
import os
setup(
    name="mjzy",
    version="0.3.9",
    author="Meijing Hou",
    author_email="houmeijing15@163.com",
    description="risk management",
    long_description="fintech545 assignment4",
    long_description_content_type="text/markdown",
    url="https://github.com/meijinghou/meijing-hou-545",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',

)
