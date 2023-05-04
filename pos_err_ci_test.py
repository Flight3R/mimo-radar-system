#%%
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

methods = [
    'analytic',
    'regression',
    'variance'
]

alpha = 0.05

for file in ['pos_err_normal', 'pos_err_phinc']:
    data = pd.read_csv(f'{file}.csv', delimiter=';')
    data = data.drop('rng_run', axis=1)
    data = data.mask(data.eq('None')).dropna()

    data['pos_err'] = data['pos_err'].astype(float)
    group = data.groupby(['method', 'phase_err'])
    mean = group.mean()
    count = group.count()
    std = group.std()
    for method in methods:
        yerr = std.loc[method] / np.sqrt(count.loc[method]) * st.t.ppf(1-alpha/2, count.loc[method] - 1)
        yerr = yerr.fillna(0)
        plot_data = mean.loc[method]
        ci_min = plot_data['pos_err'] - yerr['pos_err']
        ci_max = plot_data['pos_err'] + yerr['pos_err']
        fig, ax = plt.subplots()
        ax.plot(plot_data.index, plot_data['pos_err'])
        ax.fill_between(plot_data.index, ci_min, ci_max, alpha=0.2)
        ax.set_title(f'Position error vs phase error coefficient in {method} method. {alpha=}')
        ax.set_xlabel('Phase error coefficient [%]')
        ax.set_ylabel('Position error [m]')
        ax.set_ylim(bottom=0, top=1.1*max(plot_data['pos_err']))
        fig.savefig(f'{file}_{method}.png')
