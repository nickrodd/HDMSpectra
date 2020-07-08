# HDMSpectra
Dark Matter Spectra from the Electroweak to the Planck Scale

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-20xx.xxxxx%20-green.svg)](https://arxiv.org/abs/20xx.xxxxx)

![SpecAllM](https://github.com/nickrodd/HDMSpectra/blob/master/examples/bbbar_allM.png "Dark Matter to b-bbar to photons, all masses")

Tabulated dark matter decay and annihilation spectra for dark matter masses between the TeV and Planck scale. The spectra are similar in spirit to [PPPC4DMID](http://www.marcocirelli.net/PPPC4DMID.html), however with a number of improvements that become relevant for masses above the weak scale.

**NB:** All spectra provided are prompt, no propagation effects are included.

If these spectra are used in published work, please cite [20xx.xxxxx](https://arxiv.org/abs/20xx.xxxxx).

## Authors

- Christian Bauer
- Nicholas Rodd
- Bryan Webber

Please direct any questions or issues to nrodd@berkeley.edu.

## Installation

HDMSpectra is written entirely in python. It should be installed by executing the following command from the base directory

```
python setup.py install
```

The code is compatible with both python 2 and 3, although presentation of the examples below has been optimized for the latter. The code depends upon the following packages: [numpy](https://numpy.org/), [scipy](https://www.scipy.org/), and [h5py](https://www.h5py.org/). In most cases, the setup script above will install any missing dependencies in addition to HDMSpectra. In certain instances, the installation may fail if it is unable to download and install h5py. If you encounter this issue, manually installing h5py (using for example [pip](https://pypi.org/project/pip/): `pip install h5py`) and then attempting the HDMSpectra installation again often resolves the issue.

If you encounter any issues in the installation, please reach out to nrodd@berkeley.edu.

## Examples

A demonstration of how to access the basic features of HDMSpectra is provided [here](https://github.com/nickrodd/HDMSpectra/blob/master/examples/Functionality.ipynb). An example of how to reproduce many of the figures in [20xx.xxxxx](https://arxiv.org/abs/20xx.xxxxx) can be found [here](https://github.com/nickrodd/HDMSpectra/blob/master/examples/ReproducingPlots.ipynb).

As a minimal example, the 1 EeV spectrum in the figure above can be generated as follows

```
import numpy as np
from HDMSpectra import HDMSpectra

x = np.logspace(-4.,0.,1000)
dNdx = HDMSpectra.spec(22, 5, x, 1.e9, './data/HDMSpectra.hdf5')
```
