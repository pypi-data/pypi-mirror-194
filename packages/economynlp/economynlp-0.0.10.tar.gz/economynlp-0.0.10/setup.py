from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'Narrating Economy Using Python like a 🤖️.'

# Setting up
setup(
    name="economynlp",
    version=VERSION,
    author="Draco Deng",
    author_email="dracodeng6@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://economynlp.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'economy','intelligent economy','linguistic turn', 'linguistic'],
    classifiers=[
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Natural Language :: English'
        ]
)