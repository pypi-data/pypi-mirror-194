from setuptools import setup

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name='PyNucSeg',
    version='0.0.7',
    author="Ganesh Pandey",
    author_email="gpande3@uic.edu",
    description='Segment fluorescent nucleus, and measure the area, and the mean intensity per nucleus.',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/pganes/PyNucSeg",
    packages=['pynucseg'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
    "numpy",
    "stardist",
    "napari",
    "scikit-image",
    "tensorflow",
    ],
    extras_require ={
    "dev": [
    "pytest>=3.7",
    "twine",
    ]
    },
    

)