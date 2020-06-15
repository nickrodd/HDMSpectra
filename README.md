# HDMSpectra
Dark Matter Spectra from the Electroweak to the Planck Scale

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-20xx.xxxxx%20-green.svg)](https://arxiv.org/abs/20xx.xxxxx)

![Sensitivity](https://github.com/bsafdi/AxiScan/blob/master/examples/Projected_Sensitivity.png "Projected sensitivity versus S/N=1")


Tabulated dark matter decay and annihilation spectra for dark matter masses between the TeV and Planck scale. The spectra are similar in spirit to [PPPC4DMID](http://www.marcocirelli.net/PPPC4DMID.html), however with a number of improvements that become relevant for masses above the weak scale.

If these spectra are used in published work, please cite [20xx.xxxxx](https://arxiv.org/abs/20xx.xxxxx).

## Authors

- Christian Bauer
- Nicholas Rodd
- Bryan Webber

Please direct any questions or issues to nrodd@berkeley.edu.

## Installation

HDMSpectra is written entirely in python. It should be installed using the following command

```
python setup.py install
```

## Examples

A demonstration of using HDMSpectra to reproduce a number of figures in [20xx.xxxxx](https://arxiv.org/abs/20xx.xxxxx) is provided [here](https://github.com/nickrodd/HDMSpectra/tree/master/examples). Further documentation of all features can be found in the examples also.

As a minimal example, the 1 EeV spectrum in the figure above can be generated with

```
import numpy as np


```
