#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import warnings
import itertools

# 3rd party imports
import numpy as np

# Local imports
from ..pyrf import resample

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2021"
__license__ = "MIT"
__version__ = "2.3.7"
__status__ = "Prototype"


def eis_correlation(flux_s0, flux_s1):
    r"""Computes EIS correlaion matrix between specie 1 and specie 2,
    as described in [1]_ and [2]_ .

    Parameters
    ----------
    flux_s0 : xarray.DataArray
        Time series of the omni-directional differential particle flux of the
        first specie.
    flux_s1 : xarray.DataArray
        Time series of the omni-directional differential particle flux of the
        second specie.

    Returns
    -------
    energy_s0 : numpy.ndarray
        Energy levels of the first species.
    energy_s1 : numpy.ndarray
        Energy levels of the second species.
    corr_mat : numpy.ndarray
        Correlation matrix.

    References
    ----------
    .. [1]  Mitchell, D. G., Gkioulidou, M., & Ukhorskiy, A. Y. (2018).
            Energetic ion injections inside geosynchronous orbit:
            Convection- and drift-dominated, charge-dependent adiabatic
            energization (W = qEd). Journal of Geophysical Research: Space
            Physics, 123, 6360–6382. https://doi.org/10.1029/2018JA025556

    .. [2]  Bingham, S. T., Cohen, I. J., Mauk, B. H., Turner, D. L.,
            Mitchell, D. G., Vines, S. K., et al. (2020).
            Charge-state‐dependent energization of suprathermal ions during
            substorm injections observed by MMS in the magnetotail. Journal
            of Geophysical Research: Space Physics, 125, e2020JA028144.
            https://doi.org/10.1029/2020JA028144

    """

    ne_s0 = len(flux_s0.energy.data)
    ne_s1 = len(flux_s1.energy.data)

    corr_mat = np.zeros((ne_s0, ne_s1))

    for i, j in itertools.product(range(ne_s0), range(ne_s1)):
        ref_flux = [flux_s0, flux_s1][np.argmax([len(flux_s0), len(flux_s1)])]
        flux_s0 = resample(flux_s0, ref_flux)
        flux_s1 = resample(flux_s1, ref_flux)

        # Clean time series
        current_flux_s0 = flux_s0.data[:, i]
        current_flux_s1 = flux_s1.data[:, j]

        # Replace zeros with nan
        current_flux_s0[current_flux_s0 == 0] = np.nan
        current_flux_s1[current_flux_s1 == 0] = np.nan

        # Remove NaNs
        cond = np.logical_not(np.logical_or(np.isnan(current_flux_s0),
                                            np.isnan(current_flux_s1)))

        # det_flux_s0 = signal.detrend(current_flux_s0[cond], type="constant")
        # det_flux_s1 = signal.detrend(current_flux_s1[cond], type="constant")

        det_flux_s0 = current_flux_s0[cond]
        det_flux_s1 = current_flux_s1[cond]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            corr_mat[i, j] = np.corrcoef(det_flux_s0, det_flux_s1)[0, 1]

    # Find largest block before NaNs
    idx_max_s0 = np.max(np.where(np.logical_not(np.isnan(corr_mat)))[0]) + 1
    idx_max_s1 = np.max(np.where(np.logical_not(np.isnan(corr_mat)))[1]) + 1

    energ_s0 = flux_s0.energy.data[:idx_max_s0]
    energ_s1 = flux_s1.energy.data[:idx_max_s1]
    corr_mat = corr_mat[:idx_max_s0, :idx_max_s1]

    return energ_s0, energ_s1, corr_mat
