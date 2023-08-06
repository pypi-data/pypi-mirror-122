from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'All music of maa durga.'

# Setting up
setup(
    name="DurgaMusicAPI",
    version=VERSION,
    author="Technical Earth",
    author_email="technicalearth0@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    license_files=['LICENSE'],
    packages=find_packages(),
    install_requires=['playsound'],
    keywords=['python', 'GUI', 'app', 'tkinter', 'PyQt5', 'PYPI'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)