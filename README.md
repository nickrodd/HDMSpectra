# HDMSpectra
Dark Matter Spectra from the Electroweak to the Planck Scale

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2007.15001%20-green.svg)](https://arxiv.org/abs/2007.15001)

![SpecAllM](https://github.com/nickrodd/HDMSpectra/blob/master/examples/bbbar_allM.png "Dark Matter to b-bbar to photons, all masses")

Tabulated dark matter decay and annihilation spectra for dark matter masses between the TeV and Planck scale. The spectra are similar in spirit to [PPPC4DMID](http://www.marcocirelli.net/PPPC4DMID.html), however with a number of improvements that become relevant for masses above the weak scale.

**NB:** All spectra provided are prompt, no propagation effects are included.

If these spectra are used in published work, please cite [2007.15001](https://arxiv.org/abs/2007.15001).

## Authors

- Christian Bauer
- Nicholas Rodd
- Bryan Webber

Please direct any questions or issues to nrodd@lbl.gov.

## Installation

HDMSpectra is written entirely in python. It should be installed by executing the following command from the base directory

```
python setup.py install
```

The code is designed for use with python 3 and depends on the following packages: [numpy](https://numpy.org/), [scipy](https://www.scipy.org/), and [h5py](https://www.h5py.org/). In most cases, the setup script above will install any missing dependencies in addition to HDMSpectra. In certain instances, the installation may fail if it is unable to download and install h5py. If you encounter this issue, manually installing h5py (using for example [pip](https://pypi.org/project/pip/): `pip install h5py`) and then attempting the HDMSpectra installation again often resolves the issue.

The package can be used with python 2, although it is not recommended. The dependencies can be harder to install as pip has deprecated python 2, and so an older version of pip may be required. (Thanks to Pat Harding for drawing this to our attention.)

If you encounter any issues in the installation, please reach out to nrodd@cern.ch.

## Examples

A demonstration of how to access the basic features of HDMSpectra is provided [here](https://github.com/nickrodd/HDMSpectra/blob/master/examples/Functionality.ipynb). An example of how to reproduce many of the figures in [2007.15001](https://arxiv.org/abs/2007.15001) can be found [here](https://github.com/nickrodd/HDMSpectra/blob/master/examples/ReproducingPlots.ipynb).

As a minimal example, the 1 EeV spectrum in the figure above can be generated as follows

```
import numpy as np
from HDMSpectra import HDMSpectra

x = np.logspace(-4.,0.,1000)
dNdx = HDMSpectra.spec(22, 5, x, 1.e9, './data/HDMSpectra.hdf5')
```
