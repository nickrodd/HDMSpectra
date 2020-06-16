###############################################################################
# pclid.py
###############################################################################
# Written: Nick Rodd (Berkeley) - 15/06/20
###############################################################################
#
# Convert between particle names and pdg id codes
# 
# For polarizations, our convention is:
#  - 19: left handed (or negative helicity)
#  - 29: right handed (or positive helicity)
#  - 39: longitudinal
#
###############################################################################

import numpy as np
import six

def cid(id_f, id_i):
    """ Convert ids into the format they are stored in the FFs
        - id_f: final state id
        - id_i: initial state id
    """

    # Process final state id
    if isinstance(id_f, six.string_types):
        assert(id_f in str_f), "Unrecognized final state id"
        if id_f in str_f:
            # Convert to pdg id
            id_f = pdgid_f[np.where(id_f == str_f)][0]
    
    assert(id_f in pdgid_f), "Unrecognized final state id"
   

    # Process initial state id
    if isinstance(id_i, six.string_types):
        # If string convert to integer

        # Check if polarization information provided
        LH = False
        RH = False
        P0 = False
        if id_i[-1] == 'L':
            LH = True
            id_i = id_i[:-1]
        if id_i[-1] == 'R':
            RH = True
            id_i = id_i[:-1]
        if id_i[-1] == '0':
            P0 = True
            id_i = id_i[:-1]
        
        assert(id_i in str_i), "Unrecognized initial state id"

        id_i = upl_i[np.where(id_i == str_i)][0]
        if LH: id_i += 1900
        if RH: id_i += 2900
        if P0: id_i += 3900

    # If antiparticle (denoted by a minus), remove and append at the end
    ap = False
    if id_i < 0:
        ap = True
        id_i = -1*id_i

    # If no polarization specified, return all polarizations to be averaged
    if id_i not in upl_i:
        id_i = np.array([id_i])
    else:
        if id_i in np.array([1, 2, 3, 4, 5, 6, 11, 13, 15, 21, 22]):
            id_i = np.array([1900+id_i, 2900+id_i])
        elif id_i in np.array([12, 14, 16]):
            id_i = np.array([1900+id_i])
        elif id_i in np.array([23, 24]):
            id_i = np.array([1900+id_i, 2900+id_i, 3900+id_i])
        elif id_i in np.array([25]):
            id_i = np.array([id_i])
   
    for testi in id_i:
        assert(testi in pol_i), "Unrecognized initial state id"

    # Convert back to antiparticle
    if ap:
        assert(testi not in noap), "State has no antiparticle"
        id_i *= -1

    return id_f, id_i


################
# Particle ids #
################

# Establish allowed particle labels

# Polarized initial states (NB: no RH neutrinos)
# Fragmentation Functions are stored in terms of these states
pol_i = np.array([1901, 1902, 1903, 1904, 1905, 1906, # Q_L
                  1911, 1912, 1913, 1914, 1915, 1916, # L_L
                  2901, 2902, 2903, 2904, 2905, 2906, # Q_R
                  2911, 2913, 2915,                   # L_R
                  1921, 1922, 1923, 1924,             # V_L
                  2921, 2922, 2923, 2924,             # V_R
                  3923, 3924,                         # V_0
                  25])                                # H

# Unpolarized initial states
upl_i = np.array([1, 2, 3, 4, 5, 6,       # Q
                  11, 12, 13, 14, 15, 16, # L
                  21, 22, 23, 24,         # V
                  25])                    # H

# Initial state strings, can append with L, R or 0 to indicate pol/hel
str_i = np.array(['d', 'u', 's', 'c', 'b', 't',             # Q
                  'e', 'nue', 'mu', 'numu', 'tau', 'nutau', # L
                  'g', 'gamma', 'Z', 'W',                   # V
                  'h'])                                     # H

# States without an antiparticle
noap = np.array([1921, 1922, 1923, 2921, 2922, 2923, 3923, 25])

# Final state ids
pdgid_f = np.array([11, -11,                   # electron
                    12, -12, 14, -14, 16, -16, # neutrino
                    22,                        # photon
                    2212, -2212])              # proton

# Final state strings - a indicates antiparticle
str_f = np.array(['e', 'ae',                                         # electron
                  'nue', 'anue', 'numu', 'anumu', 'nutau', 'anutau', # neutrino
                  'gamma',                                           # photon
                  'p', 'ap'])                                        # proton
