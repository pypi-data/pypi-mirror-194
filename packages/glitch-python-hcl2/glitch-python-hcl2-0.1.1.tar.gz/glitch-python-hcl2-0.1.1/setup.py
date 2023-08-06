import os.path
from setuptools import setup, find_packages

def get_long_description():
    """Reads the long description from the README"""
    this_directory = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as file:
        return file.read()

def get_requirements():
    """Reads the installation requirements from requirements.txt"""
    with open("requirements.txt", encoding='utf8') as reqfile:
        return [line for line in reqfile.read().split("\n") if not line.startswith(('#', '-'))]

setup(
    name='glitch-python-hcl2',
    version='0.1.1',
    author='João Gonçalves',
    author_email='joao.marques.goncalves@tecnico.ulisboa.pt',
    url="https://github.com/joaotgoncalves/python-hcl2",
    license='MIT',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='',
    python_requires='>=3.7', 
    packages=find_packages(),
    description="A parser for HCL2",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=get_requirements(),
)