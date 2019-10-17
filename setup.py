import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
            
setuptools.setup(
     name='pylshvec',  
     version='0.1',
     scripts=[] ,
     install_requires=install_requires,
     author="Lizhen Shi",
     author_email="lizhen9.shi@gmail.com",
     description="LSHVec pre-trained models and its Python bindings",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Lizhen0909/PyLSHvec",
     #packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     packages=['pylshvec'],
     package_dir={'pylshvec': 'src/pylshvec'},

 )
