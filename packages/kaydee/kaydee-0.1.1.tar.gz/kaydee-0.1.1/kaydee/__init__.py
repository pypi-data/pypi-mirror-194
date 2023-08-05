import os
import numpy as np
from scipy.stats import gaussian_kde
import tqdm_pathos


## TODO
## Make bounded KDE more efficient
## Only reflect fraction f * bw of samples across boundaries
class KDE:
    
    def __init__(self, samples, bandwidth='scott', bounds=None):
        """Construct a (bounded) Gaussian kernel density estimate.
        
        Arguments
        ---------
        samples: array-like (n,) or (d, n)
            Parameter samples used to fit the KDE.
            - Univariate samples can have shape (n,) or (1, n).
            - d-dimensional samples have shape (d, n)
            
        bandwidth: str or scalar [optional, default = 'scott']
            Bandwidth to use for the Gaussian kernels.
            - Can be a string for rules of thumb 'scott' or 'silverman'.
            - A scalar constant sets the bandwidth scaling manually.
            See scipy.stats.gaussian_kde.
            
        bounds: None, bool, or array-like [optional, default = None]
            Parameter boundaries to truncate the support. The inputs samples
            are masked according to these bounds before kernel intialization.
            - A single value applies to all parameter dimensions.
            - For univariate data an array-like (2,) is allowed.
            - For multivariate data an array-like with d rows is allowed, where
              each row is either a single value or array-like (2,).
            - In all cases a None or False indicates no bound, a True
              indicates the bound is estimated from samples, while a number
              gives the location of the bound.
        """
        
        samples = np.atleast_2d(samples)
        assert samples.shape[0] < samples.shape[1]
        self.n_dim = samples.shape[0]
        
        if type(bandwidth) is str:
            bandwidth = bandwidth.lower()
            assert bandwidth == 'scott' or bandwidth == 'silverman'
        else:
            bandwidth = float(bandwidth)

        self.reflect = False
        if bounds is not None and bounds is not False:
            self.reflect = True
            self.bounds = self.get_bounds(samples, bounds)
            in_bounds = self.mask_data(samples)
            samples = samples[:, in_bounds]
            samples, self.n_reflections = self.reflect_samples(samples)
            
        self.kde = gaussian_kde(samples, bw_method=bandwidth)
        
    def pdf(self, points, splits=None, processes=1):
        """Evaluate the probability density of the KDE.
        
        Arguments
        ---------
        points: array-like (m,) or (d, m)
            Parameter locations at which to evaluate the KDE.
            - Univarate data can have shape (m,) or (1, m)
            - d-dimensional data has shape (d, n)
            
        Returns
        -------
        array-like (m,)
            Probability density evaluations at points.
        """
        
        points = np.atleast_2d(points)
        pdf = self.map_eval(self.kde.pdf, points, splits, processes)
        
        if self.reflect:
            pdf = pdf * (self.n_reflections + 1)
            in_bounds = self.mask_data(points)
            pdf[~in_bounds] = 0.0
            
        return pdf
    
    def log_pdf(self, points, splits=None, processes=1):
        """Evaluate the log probability density of the KDE.
        
        Arguments
        ---------
        points: array-like (m,) or (d, m)
            Parameter locations at which to evaluate the KDE.
            - Univarate data can have shape (m,) or (1, m)
            - d-dimensional data has shape (d, n)
            
        Returns
        -------
        array-like (m,)
            log probability density evaluations at points.
        """
        
        points = np.atleast_2d(points)
        log_pdf = self.map_eval(self.kde.logpdf, points, splits, processes)
        
        if self.reflect:
            log_pdf = log_pdf + np.log(self.n_reflections + 1)
            in_bounds = self.mask_data(points)
            log_pdf[~in_bounds] = -np.inf
            
        return log_pdf
    
    def map_eval(self, func, points, splits=None, processes=1):

        if splits is None and processes == 1:
            return func(points)

        if splits is None and processes > 1:
            splits = os.cpu_count()

        split_points = np.array_split(points, splits, axis=1)

        if processes == 1:
            split_evals = list(map(func, split_points))
        else:
            split_evals = tqdm_pathos.map(func, split_points, n_cpus=processes)

        evals = np.concatenate(split_evals)

        return evals

    def get_bounds(self, samples, bounds):
        
        if bounds is True:
            mins = np.min(samples, axis=1)
            maxs = np.max(samples, axis=1)
            _bounds = np.transpose([mins, maxs])
            
            return _bounds
        
        if self.n_dim == 1:
            assert len(bounds) == 1 or len(bounds) == 2
            if len(bounds) == 2:
                bounds = [bounds]
        else:
            assert len(bounds) == self.n_dim

        _bounds = np.zeros((self.n_dim, 2))
        for dim in range(self.n_dim):
            if bounds[dim] is None or bounds[dim] is False:
                _bounds[dim] = [-np.inf, np.inf]
            elif bounds[dim] is True:
                _bounds[dim] = [np.min(samples[dim]), np.max(samples[dim])]
            else:
                for pos in range(2):
                    if bounds[dim][pos] is None or bounds[dim][pos] is False:
                        _bounds[dim][pos] = [-np.inf, np.inf][pos]
                    elif bounds[dim][pos] is True:
                        _bounds[dim][pos] = [np.min, np.max][pos](samples[dim])
                    else:
                        _bounds[dim][pos] = float(bounds[dim][pos])
                        
        return _bounds
                
    def reflect_samples(self, samples):
                
        n_reflections = 0
        _samples = samples.copy()
        for dim in range(self.n_dim):
            for pos in range(2):
                if np.isfinite(self.bounds[dim][pos]):
                    mirror = _samples.copy()
                    mirror[dim] = 2 * self.bounds[dim][pos] - mirror[dim]
                    samples = np.concatenate((samples, mirror), axis=1)
                    n_reflections += 1
                        
        return samples, n_reflections
            
    def mask_data(self, data):
                        
        data = np.atleast_2d(data)
        above = np.all(data >= self.bounds[:, [0]], axis=0)
        below = np.all(data <= self.bounds[:, [1]], axis=0)
        
        return above * below

