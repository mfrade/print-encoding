#!/usr/bin/python3

# Tutorial:
# https://dzone.com/articles/executable-package-pip-install
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='print-encoding',
     version='1.3',
     scripts=['print-encoding'] ,
     author="Miguel Frade",
     #author_email="deepak.kumar.iet@gmail.com",
     description="Print characters in UTF-32BE, UTF-16LE and UTF-8, and unicode ranges",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/mfrade/print-encoding",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Affero General Public License v3",
         "Operating System :: OS Independent",
     ],
 )
