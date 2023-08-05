"""
Simulate critical values for finite sample distribution
and estimate asymptotic expansion parameters for the lilliefors tests
"""
import datetime as dt
import gzip
import io
import logging
import pickle
from collections import defaultdict

import numpy as np
import pandas as pd
from scipy import stats
from yapf.yapflib.yapf_api import FormatCode

import statsmodels.api as sm

NUM_SIM = 10000000
MAX_MEMORY = 2 ** 28
SAMPLE_SIZES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 25, 30, 40, 50, 100, 200, 400, 800, 1600]
MIN_SAMPLE_SIZE = {'normal': 4, 'exp': 3}
MAX_SIZE = max(SAMPLE_SIZES)
MAX_SIM_SIZE = MAX_MEMORY // (MAX_SIZE * 8)
PERCENTILES = [1, 5, 10, 25, 50, 75, 90, 92.5, 95, 97.5, 99, 99.5, 99.7, 99.9]
seed = 113682199084250344115761738871133961874
seed = np.array([(seed >> (32 * i)) % 2 ** 32 for i in range(4)],
                dtype=np.uint32)


def simulations(sim_type, save=False):
    rs = np.random.RandomState(seed)
    remaining = NUM_SIM
    results = defaultdict(list)
    start = dt.datetime.now()
    while remaining > 0:
        this_iter = min(remaining, MAX_SIM_SIZE)
        remaining -= this_iter
        if sim_type == 'normal':
            dist = rs.standard_normal
        else:
            dist = rs.standard_exponential
        rvs = dist((MAX_SIZE, this_iter))
        sample_sizes = [ss for ss in SAMPLE_SIZES if
                        ss >= MIN_SAMPLE_SIZE[sim_type]]
        for ss in sample_sizes:
            sample = rvs[:ss]
            mu = sample.mean(0)
            if sim_type == 'normal':
                std = sample.std(0, ddof=1)
                z = (sample - mu) / std
                cdf_fn = stats.norm.cdf
            else:
                z = sample / mu
                cdf_fn = stats.expon.cdf
            z = np.sort(z, axis=0)
            nobs = ss
            cdf = cdf_fn(z)
            plus = np.arange(1.0, nobs + 1) / nobs
            d_plus = (plus[:, None] - cdf).max(0)
            minus = np.arange(0.0, nobs) / nobs
            d_minus = (cdf - minus[:, None]).max(0)
            d = np.max(np.abs(np.c_[d_plus, d_minus]), 1)
            results[ss].append(d)
        logging.log(logging.INFO,
                    'Completed {0}, remaining {1}'.format(NUM_SIM - remaining,
                                                          remaining))
        elapsed = dt.datetime.now() - start
        rem = elapsed.total_seconds() / (NUM_SIM - remaining) * remaining
        logging.log(logging.INFO,
                    '({0}) Time remaining {1:0.1f}s'.format(sim_type, rem))

    for key in results:
        results[key] = np.concatenate(results[key])

    if save:
        file_name = 'lilliefors-sim-{0}-results.pkl.gz'.format(sim_type)
        with gzip.open(file_name, 'wb', 5) as pkl:
            pickle.dump(results, pkl)

    crit_vals = {}
    for key in results:
        crit_vals[key] = np.percentile(results[key], PERCENTILES)

    start = 20
    num = len([k for k in crit_vals if k >= start])
    all_x = np.zeros((num * len(PERCENTILES), len(PERCENTILES) + 2))
    all_y = np.zeros(num * len(PERCENTILES))
    loc = 0
    for i, perc in enumerate(PERCENTILES):
        y = pd.DataFrame(results).quantile(perc / 100.)
        y = y.loc[start:]
        all_y[loc:loc + len(y)] = np.log(y)
        x = y.index.values.astype(float)
        all_x[loc:loc + len(y), -2:] = np.c_[np.log(x), np.log(x) ** 2]
        all_x[loc:loc + len(y), i:(i + 1)] = 1
        loc += len(y)
    w = np.ones_like(all_y).reshape(len(PERCENTILES), -1)
    w[6:, -5:] = 3
    w = w.ravel()
    res = sm.WLS(all_y, all_x, weights=w).fit()
    params = []
    for i in range(len(PERCENTILES)):
        params.append(np.r_[res.params[i], res.params[-2:]])
    params = np.array(params)

    df = pd.DataFrame(params).T
    df.columns = PERCENTILES
    asymp_crit_vals = {}
    for col in df:
        asymp_crit_vals[col] = df[col].values

    code = '{0}_crit_vals = '.format(sim_type)
    code += str(crit_vals).strip() + '\n\n'
    code += '\n# Coefficients are model '
    code += 'log(cv) = b[0] + b[1] log(n) + b[2] log(n)**2\n'
    code += '{0}_asymp_crit_vals = '.format(sim_type)
    code += str(asymp_crit_vals) + '\n\n'
    return code


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    header = '"""\nThis file is automatically generated by ' \
             'littlefors_critical_values.py.\nDo not directly modify' \
             'this file.\n\nValue based on 10,000,000 simulations."""\n\n'
    header += 'from numpy import array\n\n'
    header += 'PERCENTILES = ' + str(PERCENTILES).strip() + '\n\n'
    header += 'SAMPLE_SIZES = ' + str(SAMPLE_SIZES).strip() + '\n\n'
    normal = simulations('normal', True)
    exp = simulations('exp', True)
    footer = """
# Critical Value
critical_values = {'normal': normal_crit_vals,
                   'exp': exp_crit_vals}
asymp_critical_values = {'normal': normal_asymp_crit_vals,
                         'exp': exp_asymp_crit_vals}

"""
    cv_filename = '../../_lilliefors_critical_values.py'
    with io.open(cv_filename, 'w', newline='\n') as cv:
        cv.write(FormatCode(header)[0])
        cv.write(FormatCode(normal)[0])
        cv.write('\n\n')
        cv.write(FormatCode(exp)[0])
        cv.write('\n\n')
        cv.write(FormatCode(footer)[0])
