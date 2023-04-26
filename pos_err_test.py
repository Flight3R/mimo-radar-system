#%%
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

data = pd.read_csv('pos_err.csv', delimiter='; ')

methods = [
    'analytic',
    'regression',
    'variance'
]

for method in methods:
    fig, ax = plt.subplots()
    curr = data.loc[data['method'] == method]
    ax.plot(curr['phase_err'], curr['pos_err'])
    ax.set_title(f"Position error vs phase error in {method} method.")
    ax.set_xlabel("Phase error coefficient [%]")
    ax.set_ylabel("Position error [m]")
    plt.savefig(f"{method}_error.png")
    plt.tight_layout()