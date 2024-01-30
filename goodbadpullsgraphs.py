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

goodvbd = pd.read_csv('goodvbdpulls.csv')
badvbd = pd.read_csv('badvbdpulls.csv')

goodrq = pd.read_csv('goodrqpulls.csv')
badrq = pd.read_csv('badrqpulls.csv')

goodchi2 = pd.read_csv('goodchi2pulls.csv')
badchi2 = pd.read_csv('badchi2pulls.csv')

good20v = pd.read_csv('good20pulls.csv')
bad20v = pd.read_csv('bad20vpulls.csv')

good25v = pd.read_csv('good25pulls.csv')
bad25v = pd.read_csv('bad25vpulls.csv')

good35v = pd.read_csv('good35pulls.csv')
bad35v = pd.read_csv('bad35vpulls.csv')

fig, ax = plt.subplots()

# overall pull graph

#ax.scatter(np.repeat(0, len(good_average)), good_average['0'], label='Average Good', color = 'blue', marker='o')

#ax.scatter(np.repeat(1, len(bad_average)), bad_average['0'], label='Average Bad', color = 'red', marker='x')

#ax.scatter(np.repeat(2, len(good_max)), good_max['0'], label='Max Good', color = 'blue', marker='o')

#ax.scatter(np.repeat(3, len(bad_max)), bad_max['0'], label='Max Bad', color = 'red', marker='x')

#ax.scatter(np.repeat(4, len(good_divergence)), good_divergence['0'], label='Divergence Good', color = 'blue', marker='o')

#ax.scatter(np.repeat(5, len(bad_divergence)), bad_divergence['0'], label='Divergence Bad', color = 'red', marker='x')

#plt.title('Pull of Good and Bad vTiles')


#for vbd pulls:

#ax.scatter(np.repeat(0, len(goodvbd)), goodvbd['Average'], label='Average Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(1, len(badvbd)), badvbd['Average'], label='Average Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(2, len(goodvbd)), goodvbd['Max'], label='Max Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(3, len(badvbd)), badvbd['Max'], label='Max Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(4, len(goodvbd)), goodvbd['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(5, len(badvbd)), badvbd['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')

#plt.title('Pull of vbd values across Good and Bad vTiles')

#for rq values:

#ax.scatter(np.repeat(0, len(goodrq)), goodrq['Average'], label='Average Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(1, len(badrq)), badrq['Average'], label='Average Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(2, len(goodrq)), goodrq['Max'], label='Max Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(3, len(badrq)), badrq['Max'], label='Max Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(4, len(goodrq)), goodrq['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(5, len(badrq)), badrq['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')

#plt.title('Pull of rq values across Good and Bad vTiles')


#ax.scatter(np.repeat(0, len(goodchi2)), goodchi2['Average'], label='Average Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(1, len(badchi2)), badchi2['Average'], label='Average Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(2, len(goodchi2)), goodchi2['Max'], label='Max Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(3, len(badchi2)), badchi2['Max'], label='Max Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(4, len(goodchi2)), goodchi2['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(5, len(badchi2)), badchi2['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')

#plt.title('Pull of chi2 values across Good and Bad vTiles')


#ax.scatter(np.repeat(0, len(good20v)), good20v['Average'], label='Average Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(1, len(bad20v)), bad20v['Average'], label='Average Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(2, len(good20v)), good20v['Max'], label='Max Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(3, len(bad20v)), bad20v['Max'], label='Max Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(4, len(good20v)), good20v['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(5, len(bad20v)), bad20v['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')

#plt.title('Pull of the current at 20v across Good and Bad vTiles')


#ax.scatter(np.repeat(0, len(good25v)), good25v['Average'], label='Average Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(1, len(bad25v)), bad25v['Average'], label='Average Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(2, len(good25v)), good25v['Max'], label='Max Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(3, len(bad25v)), bad25v['Max'], label='Max Bad', color = 'red', marker = 'x')

#ax.scatter(np.repeat(4, len(good25v)), good25v['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

#ax.scatter(np.repeat(5, len(bad25v)), bad25v['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')


#plt.title('Pull of the current at 25v across Good and Bad vTiles')


ax.scatter(np.repeat(0, len(good35v)), good35v['Average'], label='Average Good', color = 'blue', marker = 'o')

ax.scatter(np.repeat(1, len(bad35v)), bad35v['Average'], label='Average Bad', color = 'red', marker = 'x')

ax.scatter(np.repeat(2, len(good35v)), good35v['Max'], label='Max Good', color = 'blue', marker = 'o')

ax.scatter(np.repeat(3, len(bad35v)), bad35v['Max'], label='Max Bad', color = 'red', marker = 'x')

ax.scatter(np.repeat(4, len(good35v)), good35v['Divergence'], label='Divergence Good', color = 'blue', marker = 'o')

ax.scatter(np.repeat(5, len(bad35v)), bad35v['Divergence'], label='Divergence Bad', color = 'red', marker = 'x')

ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Average Good', 'Average Bad', 'Max Good', 'Max Bad', 'Divergence Good', 'Divergence Bad'])


plt.ylabel('Pull')


plt.title('Pull of the current at 35v across Good and Bad vTiles')


plt.show()

