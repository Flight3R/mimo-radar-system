#%%
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt

data = pd.read_csv('angle.csv', delimiter='; ')
print(data['angle'])


fig, ax = plt.subplots()
ax.plot(data['antenna_spread'], data['angle'])
ax.set_title("Coverage angle vs dipole spread.")
ax.set_xlabel("Dipole spread [1/wavelength]")
ax.set_ylabel("Coverage angle [deg]")
plt.tight_layout()
plt.savefig("angle.png")
