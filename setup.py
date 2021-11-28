import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pixycamev3',
    version='0.1.0',
    author='Kees Smit',
    author_email='kwsmit@hetnet.nl',
    description='Python API for Pixy2 on LEGO Mindstorms EV3',
    long_description=long_description,
    packages=['pixycamev3'],
    url='http://pypi.python.org/pypi/pixycamev3/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: ev3dev2",
    ],
)
