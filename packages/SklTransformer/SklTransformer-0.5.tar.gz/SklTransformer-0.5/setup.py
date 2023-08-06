import setuptools

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='SklTransformer',
    packages=["SklTransformer"],
    include_package_data=True,
    package_data = { "SklTransformer" : ["*"] },
    version='0.5',
    author="Kowsher",
    author_email="ga.kowsher@gmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
            'transformers==4.8.2',
            'torch==1.9.0',
            'tqdm==4.41.1',
            'numpy==1.19.5',
            'sklearn',
            
      ],
    url="https://github.com/Kowsher/SklTransformer",
    license="MIT",
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )