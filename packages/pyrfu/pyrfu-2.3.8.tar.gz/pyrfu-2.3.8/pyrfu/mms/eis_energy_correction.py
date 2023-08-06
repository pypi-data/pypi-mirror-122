#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import numpy as np

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2021"
__license__ = "MIT"
__version__ = "2.3.7"
__status__ = "Prototype"


def eis_energy_corr(vdf, gamma):
    r"""Compute energy correction factor as

    .. math::

        \\left ( \\frac{E_{eff}}{E_{g}} \\right ) = \frac{1}{\\gamma - 1}
        \\frac{r^{\\gamma - 1} - r^{-\\gamma + 1}}{r^{1} - r^{-1}}

    Parameters
    ----------
    vdf : xarray.Dataset
        Ion skymap distribution.
    gamma : float or array_like
        Power law index.

    Returns
    -------
    corr : np.ndarray
        Energy correction factor

    References
    ----------
    .. [1]  Elena A. Kronberg, Patrick W. Daly, and Esa Vilenius (2021),
            Calibration Report of the RAPID Measurements in the Cluster
            Science Archive (CSA), Version 7.0,
            url: https://caa.esac.esa.int/documents/CR/CAA_EST_CR_RAP_v70.pdf

    """

    # Unpack lower and upper bounds of the energy channels
    e_lower = vdf.energy_dminus.data
    e_upper = vdf.energy_dplus.data

    if isinstance(gamma, list):
        assert len(gamma) == len(e_lower)

    # Compute upper to lower bound energy ratio
    r = e_upper / e_lower

    # Compute correction factor
    pow_ = gamma - 1
    corr = pow_ ** -1 * (r ** pow_ - r ** -pow_) / (r ** 1 - r ** -1)
    corr = corr ** (1 / pow_)

    # Correct energies
    out = vdf.copy()
    out.energy.data *= corr

    return out
