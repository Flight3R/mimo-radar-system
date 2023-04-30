#%%
from definitions import *
import os
import glob
import time

antena1 = create_antenna_array(4, 2, 1, Position(1,2))
fig, ax = plt.subplots()
plot_scenario(ax, [antena1], TxDipole(Position(0,0)), Position(0,0))
plt.savefig('test.png')