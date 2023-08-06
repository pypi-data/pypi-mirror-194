# KnowAlmost
# See LICENSE for details.

"""
KnowAlmost API library
"""
__version__ = '1.0.1'
__author__ = ''

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="KnowAlmost",
  version="0.0.1",
  author="W·Wen",
  author_email="23626319@qq.com",
  description="KnowAlmost is a package that encapsulates the KnowAlmost api. I often use it in competitions and work. More skills are on the way!",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)