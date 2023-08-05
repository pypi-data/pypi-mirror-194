from typing import Union, Optional, List, Dict, Tuple

import math
import numpy as np

def calculate_nll(obs:float, exp:float):
    import ROOT
    return np.log(ROOT.TMath.Poisson(obs, exp))

def calculate_chi2(data_obs, data_exp, error_obs=None, threshold:float=3, epsilon:float=1e-6):
    if np.any(data_obs < 0):
        raise RuntimeError("data observed has negative-value element(s)")
    if np.any(data_exp < 0):
        raise RuntimeError("data expected has negative-value element(s)")        
    if error_obs is None:
        error_obs = np.sqrt(data_obs)
    data_obs = np.array(data_obs, dtype=np.float64)
    data_exp = np.array(data_exp, dtype=np.float64)
    error_obs = np.array(error_obs, dtype=np.float64)
    if data_obs.shape != data_exp.shape:
        raise RuntimeError("data observed and data expected have different shapes")
    if data_obs.shape != error_obs.shape:
        raise RuntimeError("data observed and error observed have different shapes")
    if data_obs.ndim != 1:
        raise RuntimeError("only one dimensional data is supported")
    chi2, chi2_last, obs_aggregate, exp_aggregate, error2_aggregate = 0., 0., 0., 0., 0.
    nbin_chi2 = 0
    bin_last = 1
    n_bins = len(data_obs)
    for i in range(n_bins):
        obs_aggregate += data_obs[i]
        exp_aggregate += data_exp[i]
        error2_aggregate += error_obs[i] ** 2
        if (obs_aggregate / np.sqrt(error2_aggregate) < threshold) or \
           (abs(obs_aggregate) < epsilon):
            if i != (n_bins - 1):
                continue
            else:
                chi2 -= chi2_last
                obs_aggregate = np.sum(data_obs[bin_last:])
                exp_aggregate = np.sum(data_exp[bin_last:])
                error2_aggregate = np.sum(error_obs[bin_last:] ** 2)
                chi2 += ((obs_aggregate - exp_aggregate) / np.sqrt(error2_aggregate)) ** 2
                if nbin_chi2 == 0:
                    nbin_chi2 += 1
        else:
            chi2_last = ((obs_aggregate - exp_aggregate) / np.sqrt(error2_aggregate)) ** 2
            bin_last = i
            chi2 += chi2_last
            nbin_chi2 += 1
            obs_aggregate, exp_aggregate, error2_aggregate = 0., 0., 0.
    # calculate likelihood
    nll, nll_last, nll_sat, nll_sat_last = 0., 0., 0., 0.
    obs_aggregate, exp_aggregate = 0., 0.
    nbin_nll = 0
    bin_last = 0
    for i in range(n_bins):
        obs_aggregate += data_obs[i]
        exp_aggregate += data_exp[i]
        error2_aggregate += error_obs[i] ** 2
        if (obs_aggregate < 2):
            if i != (n_bins - 1):
                continue
            else:
                nll -= nll_last
                nll_sat -= nll_sat_last
                obs_aggregate = np.sum(data_obs[bin_last:])
                exp_aggregate = np.sum(data_exp[bin_last:])
                nll += -1 * self.calculate_nll(obs_aggregate, exp_aggregate)
                # saturated
                nll_sat += -1 * self.calculate_nll(obs_aggregate, obs_aggregate)
                if nbin_nll == 0:
                    nbin_nll += 1
        else:
            nll_last = -1 * self.calculate_nll(obs_aggregate, exp_aggregate)
            nll_sat_last = -1 * self.calculate_nll(obs_aggregate, obs_aggregate)
            nll += nll_last
            nll_sat += nll_sat_last
            bin_last = i
            nbin_nll += 1
            obs_aggregate, exp_aggregate = 0., 0.
    result = {
        'chi2': chi2,
        'nbin_chi2': nbin_chi2,
        'nll': nll,
        'nll_sat': nll_sat,
        'nbin_nll': nbin_nll
    }
    return result

def get_poisson_interval(data:np.ndarray, n_sigma:float=1):
    """
        Calculate the Poisson error interval for binned data.
        
        Arguments:
            data: np.ndarray
                Array containing the event number in each bin.
            n_simg: float
                Number of sigma to use for the Poisson interval.
    """
    from quickstats.interface.root import TH1
    return TH1.GetPoissonError(data, n_sigma)

def get_counting_significance(s:float, b:float, sigma_b:float=0, leading_order:bool=False):
    """
        Asimov approximation for the median significance in a counting experiment.
        
        Arguments:
            s: float
                Expected number of signal events.
            b: float
                Expected number of background events.
            sigma_b: float, default = 0
                Background uncertainty. A zero value means the number of
                background events is exactly known.
            leading_order: bool, default=False
                Whether to use leading order approximation.
    """
    if sigma_b == 0:
        if leading_order:
            return s / np.sqrt(b)
        n = s + b
        return np.sqrt(2 * ((n * np.log(n / b)) - s))
    else:
        sigma_b2 = sigma_b * sigma_b
        if leading_order:
            return s / np.sqrt(b + sigma_b2)
        n = s + b
        b_plus_sigma2 = b + sigma_b2
        first_term = n * np.log((n * b_plus_sigma2)/(b * b + n * sigma_b2))
        second_term = b * b / sigma_b2 * np.log(1 + (sigma_b2 * s) / (b * b_plus_sigma2))
        return np.sqrt(2 * (first_term - second_term))
    
def get_combined_counting_significance(s:np.ndarray, b:np.ndarray,
                                       sigma_b:Union[np.ndarray, float]=0,
                                       leading_order:bool=False):
    """
        Combined significance in multiple independent counting experiments.
        
        Arguments:
            s: np.ndarray of float
                Array of expected number of signal events in each experiment.
            b: np.ndarray of float
                Array of expected number of background events in each experiment.
            sigma_b: float / np.ndarray of float, default = 0
                Array of background uncertainties in each experiment. A zero value
                means the number of background events is exactly known.
            leading_order: bool, default=False
                Whether to use leading order approximation.
    """
    if sigma_b == 0:
        if leading_order:
            Z2 = s * s / b
        else:
            n = s + b
            Z2 = 2 * ((n * np.log(n / b)) - s)
    else:
        sigma_b2 = sigma_b * sigma_b
        if leading_order:
            Z2 = s * s / (b + sigma_b2)
        else:
            n = s + b
            b_plus_sigma2 = b + sigma_b2
            first_term = n * np.log((n * b_plus_sigma2)/(b * b + n * sigma_b2))
            second_term = b * b / sigma_b2 * np.log(1 + (sigma_b2 * s) / (b * b_plus_sigma2))
            Z2 = 2 * (first_term - second_term)
    if Z2.ndim > 1:
        Z_combined = np.sqrt(np.sum(Z2, axis=Z2.ndim - 1))
    else:
        Z_combined = np.sqrt(np.sum(Z2))
    return Z_combined

def bin_edge_to_bin_center(bin_edge:np.ndarray):
    return 0.5 * (bin_edge[1:] + bin_edge[:-1])

def min_max_to_range(min_val:Optional[float]=None, max_val:Optional[float]=None):
    if (min_val is None) and (max_val is None):
        return None
    if (min_val is not None) and (max_val is not None):
        return (min_val, max_val)
    raise ValueError("min and max values must be all None or all float")

def get_hist_data(x:np.ndarray, weights:Optional[np.ndarray]=None,
                  normalize:bool=True,
                  range:Optional[Union[List, Tuple]]=None,
                  bins:int=10,
                  error_method:str="auto"):
    x = np.array(x)
    if weights is None:
        if normalize:
            weights = np.ones(x.shape) / len(x)
        y, bin_edges = np.histogram(x, bins=bins, range=range, weights=weights)
        bin_centers = bin_edge_to_bin_center(bin_edges)
        hist_data = {
            "x"    : bin_centers,
            "y"    : y,
            "xerr" : None,
            "yerr" : None
        }
    else:
        weights = np.array(weights)
        error_method = error_method.lower()
        assert error_method in ["sumw2", "poisson", "auto"]
        if error_method == "auto":
            unit_weight = np.allclose(weights, np.ones(weights.shape))
            error_method = "poisson" if unit_weight else "sumw2"
        if normalize:
            size = weights.sum()
        else:
            size = 1
        if error_method == "poisson":
            _y, bin_edges = np.histogram(x, bins=bins, range=range, weights=weights)
            from quickstats.maths.statistics import get_poisson_interval
            pois_interval = get_poisson_interval(_y)
            yerr =  (pois_interval["lo"] / size, pois_interval["hi"] / size)
            _weights = weights / size
            y, bin_edges = np.histogram(x, bins=bins, range=range, weights=_weights)
        elif error_method == "sumw2":
            _y, bin_edges = np.histogram(x, bins=bins, range=range, weights=weights**2)
            _weights = weights / size
            y, bin_edges = np.histogram(x, bins=bins, range=range, weights=_weights)
            yerr = np.sqrt(_y) / size
        bin_centers = bin_edge_to_bin_center(bin_edges)
        xerr = (bin_centers[1] - bin_centers[0])/2
        hist_data = {
            "x"    : bin_centers,
            "y"    : y,
            "xerr" : xerr,
            "yerr" : yerr
        }
    return hist_data
    