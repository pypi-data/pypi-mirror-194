from setuptools import setup, find_packages
import os
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'MDML',
    version= "0.0.1",
    author= "Stylianos Mavrianos", 
    author_email= "stylianosmavrianos@gmail.com", 
    description= 'Application of Deep learning on molecular dymanamics trajectories',
    packages= find_packages(),
    url = "https://github.com/StevetheGreek97/MD_ML.git",
    # long_description=read('README.md'),
    install_requires = read('requirements.txt'),
    classifiers=[
        "Programming Language :: Python", 
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Intended Audience :: Education"
        
    ] 
     
)