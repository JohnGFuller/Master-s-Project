from ds20kdb import interface;
dbi = interface.Database(); 

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

good_average = pd.read_csv('good_averages.csv')
good_max = pd.read_csv('good_max.csv')
good_divergence = pd.read_csv('good_divergence.csv')

bad_average = pd.read_csv('bad_averages.csv')
bad_max = pd.read_csv('bad_max.csv')
bad_divergence = pd.read_csv('bad_divergence.csv')

fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(good_average)), good_average['0'], label='Average Good', color = 'blue', marker='o')

ax.scatter(np.repeat(1, len(bad_average)), bad_average['0'], label='Average Bad', color = 'red', marker='x')

ax.scatter(np.repeat(2, len(good_max)), good_max['0'], label='Max Good', color = 'blue', marker='o')

ax.scatter(np.repeat(3, len(bad_max)), bad_max['0'], label='Max Bad', color = 'red', marker='x')

ax.scatter(np.repeat(4, len(good_divergence)), good_divergence['0'], label='Divergence Good', color = 'blue', marker='o')

ax.scatter(np.repeat(5, len(bad_divergence)), bad_divergence['0'], label='Divergence Bad', color = 'red', marker='x')

ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Average Good', 'Average Bad', 'Max Good', 'Max Bad', 'Divergence Good', 'Divergence Bad'])

plt.ylabel('Pull')
plt.title('Pull of Good and Bad vTiles')
plt.show()
