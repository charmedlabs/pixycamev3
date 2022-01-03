import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pixycamev3',
    version='1.0.0',
    author='Kees Smit',
    author_email='kwsmit@hetnet.nl',
    description='Python3 API for Pixy2 on LEGO Mindstorms EV3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pixycamev3'],
    url='https://github.com/charmedlabs/pixycamev3',
    project_urls = {
        'Documentation': 'https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:python',
        'Bug tracker': 'https://github.com/charmedlabs/pixycamev3/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 5 - Production/Stable"
    ],
)
