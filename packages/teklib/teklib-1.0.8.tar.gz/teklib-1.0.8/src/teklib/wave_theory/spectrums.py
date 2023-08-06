import numpy as np

def jonswap(f:np.ndarray, Hm0:float, Tp:float, gamma:float=3.3, sigma_low:float=.07, sigma_high:float=.09,
            g:float=9.81, method:str='yamaguchi', normalize:bool=False):
    '''Generate JONSWAP spectrum using a function
    taken from https://github.com/openearth/oceanwaves-python/blob/master/oceanwaves/spectral.py
    and then simplified (temporary solution to circumvent the need to use WAFO). Checked against
    wafo for specified gamma
    
    TODO: Set gamma's default value to one based on a formula
    
    To use:
    >> from teklib.wave_theory.spectrums import jonswap
    >> import matplotlib.pyplot as plt
    >> plt.plot(f, jonswap(f, 10, 15))
    >> plt.show()
    
    Parameters
    ----------
    f : numpy.ndarray
        Array of frequencies [Hz]
    Hm0 : float, numpy.ndarray
        Required zeroth order moment wave height
    Tp : float, numpy.ndarray
        Required peak wave period
    gamma : float
        JONSWAP peak-enhancement factor (default: 3.3)
    sigma_low : float
        Sigma value for frequencies <= ``1/Tp`` (default: 0.07)
    sigma_high : float
        Sigma value for frequencies > ``1/Tp`` (default: 0.09)
    g : float
        Gravitational constant (default: 9.81)
    method : str
        Method to compute alpha (default: yamaguchi)
    normalize : bool
        Normalize resulting spectrum to match ``Hm0``
    Returns
    -------
    E : numpy.ndarray
        Array of shape ``f, Hm0.shape`` with wave energy densities
    '''

    # Pierson-Moskowitz
    if method.lower() == 'yamaguchi':
        alpha = 1. / (.06533 * gamma ** .8015 + .13467) / 16.
    elif method.lower() == 'goda':
        alpha = 1. / (.23 + .03 * gamma - .185 / (1.9 + gamma)) / 16.
    else:
        raise ValueError('Unknown method: %s' % method)

    E_pm = alpha * Hm0**2 * Tp**-4 * f**-5 * np.exp(-1.25 * (Tp * f)**-4)

    # JONSWAP
    sigma = np.ones(f.shape) * sigma_low
    sigma[f > 1./Tp] = sigma_high

    E_js = E_pm * gamma**np.exp(-0.5 * (Tp * f - 1)**2. / sigma**2.)

    if normalize:
        # axis=0 seems to work fine with all kinds of inputs
        E_js *= Hm0**2. / (16. * np.trapz(E_js, f, axis=0))

    return E_js