from ds20kdb import interface; 
dbi = interface.Database(); 

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import csv

df = pd.read_csv('/data/jfuller/vtile_passport_f.csv', delimiter = ',')

vbd = dbi.get('sipm_test',sipm_qc_id=9).data.vbd 
vbd_mean = vbd.mean() 

rq = dbi.get('sipm_test', sipm_qc_id=11).data.rq
rq = rq[(rq >= 0) & (rq <= 100)]
rq_mean = rq.mean()

chi2 = dbi.get('sipm_test', sipm_qc_id=11).data.chi2_shape
chi2 = chi2[(chi2 <= 25)] 
chi2_mean = chi2.mean() 

i_20v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_20v 
i_20v = i_20v[(i_20v <= 60e-12)] 
i_20v_mean = i_20v.mean() 

i_25v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_25v 
i_25v = i_25v[(i_25v <= 70e-12)] 
i_25v_mean = i_25v.mean() 

i_35v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_35v 
i_35v = i_35v[(5e-11 <= i_35v)] 
i_35v_mean = i_35v.mean() 

good_tiles = df[df['quality'] == 'Good']
bad_tiles = df[df['quality'] == 'Bad']


good_average = []
good_max = []
good_std = []

for index, row in good_tiles.iterrows():	
	qrcode = row['QR code']
	vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data	

	pulls = []
		
	for sipm_id in range(1,25):
	

						
		sipm_data = dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1] 
		vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1] 
		rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1] 
		chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
		i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1] 
		i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1] 
		i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1] 
  

		vbd_pull = abs((vbd_sipm - vbd_mean) / vbd_mean)
		rq_pull =  abs((rq_sipm - rq_mean) / rq_mean) 
		chi2_pull =  abs((chi2_sipm - chi2_mean) / chi2_mean) 
		i_20v_pull =  abs((i_20v_sipm - i_20v_mean) / i_20v_mean) 
		i_25v_pull =  abs((i_25v_sipm - i_25v_mean) / i_25v_mean) 
		i_35v_pull =  abs((i_35v_sipm - i_35v_mean) / i_35v_mean) 

		
		pull = abs((vbd_pull + rq_pull + chi2_pull + i_20v_pull + i_25v_pull + i_35v_pull)/6) 
		pulls.append(pull)
	
	pull_average = np.mean(pulls)
	good_average.append(pull_average)
		
	pull_max = np.max(pulls)
	good_max.append(pull_max)

	pull_std = np.std(pulls)
	good_std.append(pull_std)

		


bad_average = []
bad_max = []
bad_std = []

for index, row in bad_tiles.iterrows():
	qrcode = row['QR code']
	vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data

	pulls = []

	for sipm_id in range(1,25):


		sipm_data =  dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1]

		vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1]
		rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1]
		chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
		i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1]
		i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1]
		i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1]

		vbd_pull = abs((vbd_sipm - vbd_mean) / vbd_mean)
		rq_pull =  abs((rq_sipm - rq_mean) / rq_mean)
		chi2_pull =  abs((chi2_sipm - chi2_mean) / chi2_mean)
		i_20v_pull =  abs((i_20v_sipm - i_20v_mean) / i_20v_mean)
		i_25v_pull = abs((i_25v_sipm - i_25v_mean) / i_25v_mean)
		i_35v_pull =  abs((i_35v_sipm - i_35v_mean) / i_35v_mean)

		pull = abs((vbd_pull + rq_pull + chi2_pull + i_20v_pull + i_25v_pull + i_35v_pull)/6)
		pulls.append(pull)

	pull_average = np.mean(pulls)
	bad_average.append(pull_average)

	pull_max = np.max(pulls)		
	bad_max.append(pull_max)

	pull_std = np.std(pulls)
	bad_std.append(pull_std)



df_g_average = pd.DataFrame(good_average)
df_g_average.to_csv('good_averages.csv', index=False)

df_g_max = pd.DataFrame(good_max)
df_g_max.to_csv('good_max.csv', index=False)

df_g_std = pd.DataFrame(good_std)
df_g_std.to_csv('good_divergence.csv', index=False)

df_b_average = pd.DataFrame(bad_average)
df_b_average.to_csv('bad_averages.csv', index=False)

df_b_max = pd.DataFrame(bad_max)
df_b_max.to_csv('bad_max.csv', index=False)

df_b_std = pd.DataFrame(bad_std)
df_b_std.to_csv('bad_divergence.csv', index=False)

