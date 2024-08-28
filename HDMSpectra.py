###############################################################################
# HDMSpectra.py
###############################################################################
# Written: Nick Rodd (Berkeley) - 15/06/20
###############################################################################
#
# Generate the spectrum of Heavy Dark Matter (decays or annihilation)
#
# Can also be used to compute individual fragmentation functions 
#
###############################################################################

from __future__ import print_function

from os import path
import numpy as np
from scipy.interpolate import interp1d, RegularGridInterpolator
import h5py
import copy

from .pclid import cid

def spec(finalstate, X, xvals, mDM, data, 
         annihilation=False, Xbar=None, delta=False,
         interpolation='cubic'):
    """ Compute spectrum per decay (or per annihilation) of heavy dark matter
        Process computed is DM(+DM) -> X Xbar -> finalstate
        - finalstate: stable Standard Model state, provide as a string or pdgid
        - X: initial state, provide as a string or pdgid
        - xvals: array of energy fractions (2E/mDM for decay or E/mDM for ann)
        - mDM: Dark Matter mass [GeV]
        - data: string point to the hdf5 data that ships with the github package
        - annihilation: by default assume decay, if annihilation set True
        - Xbar: by default assume Xbar = conjugate(X), but can specify manually
                in the same format as X
        - delta: append the delta function coefficient for the process as the
                 last entry in dN/dx
        - interpolation: the kind of interpolation to use between the provided
                         data points, either cubic or linear

        return: dN/dx
    """

    # Confirm data file is at the specified location
    assert (path.exists(data)), \
        "data must point to the provided HDMSpectra.hdf5"

    # Determine Q value according to the process
    if annihilation: Qval = mDM
    else: Qval = mDM/2.

    # Convert states to pdg ids
    id_fs, id_is = cid(finalstate, X)
    if Xbar == None: # Assume Xbar = conjugate(X)
        # If Xbar = X, will simply multiply spectrum by 2
        if id_is[0] not in noap:
            id_is = np.append(id_is, -id_is)
    else:
        _, id_is_bar = cid(finalstate, Xbar)
        id_is = np.append(id_is, id_is_bar)


    # Extract the spectrum for each
    if len(np.shape(xvals)) == 0: xvals = np.array([xvals])
    dNdx = np.zeros_like(xvals)
    if delta: 
        dNdx = np.append(dNdx, 0.)

    for high_id in id_is:
        dNdx += FF(id_fs, high_id, xvals, Qval, data, delta=delta, 
                   interpolation=interpolation)

    # Average over polarizations (2 for X + Xbar)
    dNdx /= float(len(id_is))/2.

    # Check for the presence of negative dN/dx values
    # These result from the cubic interpolation of points near 0
    if np.min(dNdx) < 0.:
        negloc = np.where(dNdx < 0.)
        dNdx[negloc] = 0.
        print("Negative dN/dx values were set to 0 for the following x:")
        print(xvals[negloc])
        print("Caution around these values should be taken")
        print("A comparison with linear interpolation is recommended")
    
    return dNdx


def FF(id_f, id_i, xvals, Qval, data, delta=False, interpolation='cubic'):
    """ Compute Fragmentation Function
        - id_f: final state id
        - id_i: initial state id
        - xvals: array of energy fractions to evaluate FF at 
        - Qval: virtuality scale initial [GeV]
        - data: string point to the hdf5 data that ships with the github package
        - delta: append the delta function coefficient for the process as the
                 last entry in dN/dx
        - interpolation: the kind of interpolation to use between the provided
                         data points, either cubic or linear

        return: dN/dx
    """

    # Confirm input x and Q values in the allowed range
    assert((np.min(xvals) >= 1.e-6) & (np.max(xvals) <= 1.)), \
        "x array extends outside allowed range of [1.e-6, 1.]"
    if len(np.shape(xvals)) == 0: xvals = np.array([xvals])

    assert((Qval >= 500.) & (Qval <= 1.e19)), \
        "Q outside allowed range of [500, 1.e19] GeV"

    # Process input ids
    id_f, id_i = cid(id_f, id_i)

    # If final state is a proton, calculate an array of momentum fractions
    # and then account for the finite mp
    if id_f in np.array([2212, -2212]):
        xvals_p = copy.deepcopy(xvals)
        xvals = np.logspace(-6,0.,1000)

    # Determine spectra for each initial state
    dNdx = np.zeros_like(xvals)
    delta_coeff = 0.

    f = h5py.File(data, 'r')
    for high_id in id_i:
        # Load tabulated spectra - will interpolate to our specific value
        xtab, Qtab, Ftab = unpackFF(id_f, high_id, f)

        # Interpolate to the relevant values
        # Adjust zero value to be 1.e-6
        xtab0 = np.copy(xtab)
        xtab0[0] = 1.e-6
        FF_int = RegularGridInterpolator((Qtab, xtab0), Ftab, method=interpolation)

        # FF is d(x) = x*dNdx
        dNdx += FF_int((np.log10(Qval), xvals))/xvals

        if delta:
            delta_coeff += unpackdelta(id_f, high_id, f, Qval, 
                                       interpolation=interpolation)

    f.close()
    
    dNdx /= float(len(id_i)) # Average over polarizations/helicities
    delta_coeff /= float(len(id_i))

    # Account for proton mass
    if id_f in np.array([2212, -2212]):
        # Determine proton energy fractions
        xp_E = np.sqrt(Qval**2.*xvals**2.+mp**2.)/Qval
        rescale = (xp_E/xvals)*(xvals/xp_E)**k

        if np.min(xp_E) > 1.e-6:
            xp_E = np.append(1.e-6, xp_E)
            dNdx = np.append(0., dNdx)
            rescale = np.append(0., rescale)
        
        dNdx_int = interp1d(xp_E, rescale*dNdx, kind='cubic')
        dNdx = dNdx_int(xvals_p)
        # Remove values below mp/Q
        xforbid = np.where(xvals_p < mp/Qval)
        dNdx[xforbid] = 0.

    if delta:
        dNdx = np.append(dNdx, delta_coeff)
    
    return dNdx


def unpackFF(id_f, id_i, f):
    """ Extract relevant arrays of x, Q, and FF for specified IDs
        - id_f: final state pdg id
        - id_i: initial state polarized pdg id
        - f: h5py file
    """
    
    g = f['high_gauge']
    gid = g['high_flavors']

    h = f['high_higgs']
    hid = h['high_flavors']

    l = f['high_leptons']
    lid = l['high_flavors']

    q = f['high_quarks']
    qid = q['high_flavors']

    # Extract the relevant array of values
    if id_i in gid:
        loc = np.where(id_i == gid)[0][0]
        xarr = g['x_'+str(id_f)]
        Qarr = g['Q_'+str(id_f)]
        Farr = g['FF_'+str(id_f)][loc]
    if id_i in hid:
        loc = np.where(id_i == hid)[0][0]
        xarr = h['x_'+str(id_f)]
        Qarr = h['Q_'+str(id_f)]
        Farr = h['FF_'+str(id_f)][loc]
    if id_i in lid:
        loc = np.where(id_i == lid)[0][0]
        xarr = l['x_'+str(id_f)]
        Qarr = l['Q_'+str(id_f)]
        Farr = l['FF_'+str(id_f)][loc]
    if id_i in qid:
        loc = np.where(id_i == qid)[0][0]
        xarr = q['x_'+str(id_f)]
        Qarr = q['Q_'+str(id_f)]
        Farr = q['FF_'+str(id_f)][loc]

    return xarr, Qarr, Farr


def unpackdelta(id_f, high_id, f, Qval, interpolation='cubic'):
    """ Extract relevant arrays of x, Q, and FF for specified IDs
        - id_f: final state pdg id
        - id_i: initial state polarized pdg id
        - f: h5py file
        - Qval: virtuality scale initial [GeV]
        - interpolation: the kind of interpolation to use between the provided
                         data points, either cubic or linear
    """

    check_delta = str(high_id) + '_2_' + str(id_f)

    if check_delta in delta_str:
        d = f['delta_coeff']
        Qarr = d['Q']
        darr = d[check_delta]
        d_int = interp1d(Qarr, darr, kind=interpolation)

        return d_int(np.log10(Qval))
    else:
        return 0.


# List of states without an antiparticle
noap = np.array([1921, 1922, 1923, 2921, 2922, 2923, 3923, 25])

# List of transitions with a non-zero delta-fn coefficient
# Format: highid_2_lowid
delta_str = np.array(['1911_2_11', '-1911_2_-11', # eL -> e 
                      '2911_2_11', '-2911_2_-11', # eR -> e
                      '1912_2_12', '-1912_2_-12', # nue -> nue
                      '1914_2_14', '-1914_2_-14', # numu -> numu
                      '1916_2_16', '-1916_2_-16', # nutau -> nutau
                      '1922_2_22', '2922_2_22',   # gamma -> gamma
                      '1923_2_22', '2923_2_22'])  # ZT -> gamma

# Details for the proton mass calculation
k = 3 # index of the power correction
mp = 0.9382720813 # [GeV]
