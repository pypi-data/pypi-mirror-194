from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Find the "n-th" working day of a month'
LONG_DESCRIPTION = 'A package that allows to find n-th business day of a month.'

# Setting up
setup(
    name="nth_Bday",
    version=VERSION,
    author="u77w41 (Ujjwal Chowdhury)",
    author_email="<u77w41@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'datetime', 'holidays'],
    keywords=['python', 'date', 'Business Day', 'Working Day', 'Holiday', 'calender'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)