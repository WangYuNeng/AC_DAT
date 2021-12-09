from setuptools import setup

setup(
   name='AC_SAT',
   description='Implemeting ACSAT in https://ieeexplore.ieee.org/abstract/document/8203858',
   author='Yu-Neng Wang',
   author_email='wynwyn@stanford.edu',
   packages=['AC_SAT'],
   install_requires=['scipy', 'matplotlib', 'tqdm']
)