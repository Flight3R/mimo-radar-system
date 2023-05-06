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

ph_inc = [
    False,
    True
]

alpha = 0.05

data = pd.read_csv(f'pos_err.csv', delimiter=';')

data = data.drop('rng_run', axis=1)
data = data.mask(data.eq('None')).dropna()
data['pos_err'] = data['pos_err'].astype(float)

group = data.groupby(['method', 'phase_increment', 'phase_err'])

mean = group.mean()
count = group.count()
std = group.std()

for mt in methods:
    for pi in ph_inc:
        yerr = std.loc[mt, pi] / np.sqrt(count.loc[mt, pi]) * st.t.ppf(1-alpha/2, count.loc[mt, pi] - 1)

        yerr = yerr.fillna(0)

        plot_data = mean.loc[mt, pi]

        ci_min = plot_data['pos_err'] - yerr['pos_err']
        ci_max = plot_data['pos_err'] + yerr['pos_err']

        fig, ax = plt.subplots()
        ax.set_xlabel('Phase error coefficient [%]')
        ax.set_ylabel('Position error [m]')
        ax.plot(plot_data.index*100, plot_data['pos_err'])
        ax.fill_between(plot_data.index*100, ci_min, ci_max, alpha=0.2)
        ax.set_ylim(bottom=0, top=1.1*max(plot_data['pos_err']))
        fig.savefig(f'{mt}{"_pi" if pi else ""}.png')
