from distutils.core import setup
from setuptools import find_packages

setup(name='sam-learner',
      version='1.10.2',
      python_requires=">=3.8",
      description='Safe Action Model Learner',
      author='Argaman Mordoch',
      packages=find_packages(exclude=["tests", "utils"]),
     )