from setuptools import setup
import codecs
import os

VERSION = '0.0.8'
DESCRIPTION = 'Local file updater'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name='file-updater',
    version=VERSION,
    author='Daniel Riffert',
    author_email='riffert.daniel@gmail.com',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    package_dir={'':'src'},
    packages=['fup'],
    scripts=['src/lofup.py'],
    install_requires=['colorama', 'pywin32'],
    keywords=['file', 'update', 'path', 'backup'],
    platforms=['windows']
)