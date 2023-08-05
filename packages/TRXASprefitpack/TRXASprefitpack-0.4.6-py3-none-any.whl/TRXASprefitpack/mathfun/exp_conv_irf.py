'''
exp_conv_irf:
submodule for the mathematical functions for 
exponential decay convolved with irf

:copyright: 2021 by pistack (Junho Lee).
:license: LGPL3.
'''

import numpy as np
from scipy.special import erfc, erfcx, exp1


def exp_conv_gau(t, fwhm, k):

    '''
    Compute exponential function convolved with normalized gaussian 
    distribution

    Note.
    We assume temporal pulse of x-ray is normalized gaussian distribution
    
    .. math::

       \sigma = \\frac{fwhm}{2\sqrt{2\log{2}}}


    .. math::

       IRF(t) = \\frac{1}{\\sigma \\sqrt{2\pi}}\\exp\\left(-\\frac{t^2}{2\\sigma^2}\\right)

    :param t: time
    :type t: float, numpy_1d_array
    :param fwhm: full width at half maximum of x-ray temporal pulse
    :type fwhm: float
    :param k: rate constant (inverse of life time)
    :type k: float

    
    :return: convolution of normalized gaussian distribution and exp(-kt)

    .. math::

       \\frac{1}{2}\exp\\left(\\frac{k^2}{2\sigma^2}-kt\\right){erfc}\\left(\\frac{1}{\sqrt{2}}\\left(k\sigma-\\frac{t}{\sigma}\\right)\\right)


    :rtype: numpy_1d_array
    '''

    sigma = fwhm/(2*np.sqrt(2*np.log(2)))
    ksigma = k*sigma
    ksigma2 = ksigma*sigma
    tinvsigma = t/sigma

    if not isinstance(t, np.ndarray):
        if ksigma2 > t:
            ans = 1/2*np.exp(-0.5*tinvsigma**2) * \
                erfcx(1/np.sqrt(2)*(ksigma-tinvsigma))
        else:
            ans = 1/2*np.exp(k*(0.5*ksigma2-t)) * \
                erfc(1/np.sqrt(2)*(ksigma - tinvsigma))
    else:
        mask = t < ksigma2
        inv_mask = np.invert(mask)
        ans = np.zeros(t.shape[0])
        ans[mask] = 1/2*np.exp(-0.5*tinvsigma[mask]**2) * \
            erfcx(1/np.sqrt(2)*(ksigma-tinvsigma[mask]))
        ans[inv_mask] = 1/2*np.exp(k*(0.5*ksigma2-t[inv_mask])) * \
            erfc(1/np.sqrt(2)*(ksigma - tinvsigma[inv_mask]))

    return ans


def exp_conv_cauchy(t, fwhm, k):

    '''
    Compute exponential function convolved with normalized cauchy 
    distribution

    Note.
    We assume temporal pulse of x-ray is normalized cauchy distribution

    .. math::
       \\gamma = \\frac{fwhm}{2}

    .. math::
       IRF(t) = \\frac{\\gamma}{\\pi}\\frac{1}{(x-t)^2+\\gamma^2}
    

    :param t: time
    :type t: float, numpy_1d_array
    :param fwhm: full width at half maximum of x-ray temporal pulse
    :type fwhm: float
    :param k: rate constant (inverse of life time)
    :type k: float

   
    :return: convolution of normalized cauchy distribution and exp(-kt)

    .. math::
       \\frac{\\exp(-kt)}{\\pi}\\Im\\left(\\exp(-ik\\gamma)\cdot{E1}(-kt-ik\\gamma)\\right)


    :rtype: numpy_1d_array 
    '''

    gamma = fwhm/2
    if k == 0:
        ans = 0.5+1/np.pi*np.arctan(t/gamma)
    else:
        ikgamma = complex(0, k*gamma)
        kt = k*t
        if not isinstance(t, np.ndarray):
            if np.abs(kt) < 700:
                ans = np.exp(-ikgamma)*exp1(-kt-ikgamma)
                ans = np.exp(-kt)*ans.imag/np.pi
            else:
                inv_z = 1/(kt+ikgamma)
                ans = 1+10*inv_z
                ans = 1+9*inv_z*ans
                ans = 1+8*inv_z*ans
                ans = 1+7*inv_z*ans
                ans = 1+6*inv_z*ans
                ans = 1+5*inv_z*ans
                ans = 1+4*inv_z*ans
                ans = 1+3*inv_z*ans
                ans = 1+2*inv_z*ans
                ans = 1+inv_z*ans
                ans = -inv_z*ans
                ans = ans.imag/np.pi
        else:
            mask = np.abs(kt) < 700
            inv_mask = np.invert(mask)
         
            ans = np.zeros(t.shape[0], dtype='float')
            inv_z = 1/(kt[inv_mask]+ikgamma)

            # abs(kt) < 700
            ans1 = np.exp(-ikgamma)*exp1(-kt[mask]-ikgamma)
            ans[mask] = np.exp(-kt[mask])*ans1.imag/np.pi

            # abs(kt) > 700, use asymptotic series
            ans2 = 1+10*inv_z
            ans2 = 1+9*inv_z*ans2
            ans2 = 1+8*inv_z*ans2
            ans2 = 1+7*inv_z*ans2
            ans2 = 1+6*inv_z*ans2
            ans2 = 1+5*inv_z*ans2
            ans2 = 1+4*inv_z*ans2
            ans2 = 1+3*inv_z*ans2
            ans2 = 1+2*inv_z*ans2
            ans2 = 1+1*inv_z*ans2
            ans2 = -inv_z*ans2
            ans[inv_mask] = ans2.imag/np.pi
    return ans


def exp_conv_pvoigt(t, fwhm_G, fwhm_L, eta, k):

    '''
    Compute exponential function convolved with normalized pseudo
    voigt profile

    Note.
    We assume temporal pulse of x-ray is pseudo voigt profile

    .. math::
       \mathrm{pvoigt}(t) = (1-\\eta)G({fwhm}_G, t)+\\eta C({fwhm}_L, t)
    

    :param t: time
    :type t: float, numpy_1d_array
    :param fwhm_G: full width at half maximum of x-ray temporal pulse gaussian part
    :type fwhm_G: float
    :param fwhm_L: full width at half maximum of x-ray temporal pulse cauchy part
    :type fwhm_L: float
    :param eta: mixing parameter
    :type eta: float
    :param k: rate constant (inverse of life time)
    :type k: float

   
    :return: convolution of normalized pseudo voigt profile and exp(-kt)
    :rtype: numpy_1d_array 
    '''

    return eta*exp_conv_cauchy(t, fwhm_L, k) + \
        (1-eta)*exp_conv_gau(t, fwhm_G, k)
