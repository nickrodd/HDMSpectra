from setuptools import setup

setup(name='HDMSpectra',
   version='1.0',
   description='Dark Matter Spectra from the Electroweak to the Planck Scale',
   author='Nicholas L Rodd',
   author_email='nrodd@berkeley.edu',
   url='https://github.com/nickrodd/HDMSpectra',
   license='MIT',
   packages=['HDMSpectra'],  
   install_requires=['numpy', 'matplotlib', 'h5py', 'jupyter', 'scipy', 'six'],
)
