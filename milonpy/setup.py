#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on Feb 24, 2013
@author: nickmilon
see: https://docs.python.org/2/distutils/setupscript.html
'''
from setuptools  import setup, find_packages
#from __init__ import __version__ 
__version__ ="1.0.1"
setup(
    #packages=find_packages(), #package_dir = {'milonpy': 'milonpy'}, 
    packages=["milonpy"],  
    package_data={'mongo_vs_es': ['sample_data/*.txt']},
    name="milonpy",
    version=__version__,
    author="nickmilon",
    #author_email="nickmilon@gmail.com",
    maintainer="nickmilon",
    maintainer_email="*@gmail.com",
    url="https://github.com/nickmilon/milonpy",
    description="python utilities",
    long_description="see: readme",
    download_url="https://github.com/nickmilon/milonpy.git",
    classifiers=[
    "Development Status :: ",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 2.7",
    "Topic :: Database"],
    #platforms =
    license="Apache License, Version 2.0",
    keywords=["python", "utilities"],
    # requirements and specs
    zip_safe=False,
    tests_require=["nose"], 
    install_requires=[]
)
print "setup installed packages:",find_packages()  
