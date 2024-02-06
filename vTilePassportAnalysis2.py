from ds20kdb import interface
dbi = interface.Database();
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_csv('/data/jfuller/vtile_passport_f.csv', delimiter=',')

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

# defining the passing and failing rows for each variable in the passport

passedsnr = df[~df['snr'].str.contains('\*')]
failedsnr = df[df['snr'].str.contains('\*')]

passedamplitude_1pe = df[~df['amplitude_1pe'].str.contains('\*')]
failedamplitude_1pe = df[df['amplitude_1pe'].str.contains('\*')]

passeddark_noise = df[~df['dark_noise'].str.contains('\*')]
faileddark_noise = df[df['dark_noise'].str.contains('\*')]

passedcda = df[~df['cda'].str.contains('\*')]
failedcda = df[df['cda'].str.contains('\*')]

passedrms = df[~df['rms'].str.contains('\*')]
failedrms = df[df['rms'].str.contains('\*')]

passedapa = df[~df['apa'].str.contains('\*')]
failedapa = df[df['apa'].str.contains('\*')]

# obtaining the qc values for the respective passport variables

snrpass_vbd_mean = []
snrpass_vbd_max = []
snrpass_vbd_div = []

snrpass_rq_mean = []
snrpass_rq_max = []
snrpass_rq_div = []

snrpass_chi2_mean = []
snrpass_chi2_max = []
snrpass_chi2_div = []

snrpass_i_20v_mean = []
snrpass_i_20v_max = []
snrpass_i_20v_div = []

snrpass_i_25v_mean = []
snrpass_i_25v_max = []
snrpass_i_25v_div = []

snrpass_i_35v_mean = []
snrpass_i_35v_max = []
snrpass_i_35v_div = []


for index, row in passedapa.iterrows():
	qrcode = row['QR code']
	vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data
	
	vbd_pull_array = []
	rq_pull_array = []
	chi2_pull_array = []
	i_20v_pull_array = []
	i_25v_pull_array = []
	i_35v_pull_array = []

	for sipm_id in range(1,25):

		sipm_data = dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1] 

		vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1]
		vbd_pull = (vbd_sipm - vbd_mean) / vbd_mean
		vbd_pull_array.append(vbd_pull)

		rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1] 
		rq_pull = (rq_sipm - rq_mean) / rq_mean
		rq_pull_array.append(rq_pull)

		chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
		chi2_pull = (chi2_sipm - chi2_mean) / chi2_mean
		chi2_pull_array.append(chi2_pull)

		i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1] 
		i_20v_pull = (i_20v_sipm - i_20v_mean) / i_20v_mean
		i_20v_pull_array.append(i_20v_pull)
		
		i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1] 
		i_25v_pull = (i_25v_sipm - i_25v_mean) / i_25v_mean
		i_25v_pull_array.append(i_25v_pull)

		i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1] 
		i_35v_pull = (i_35v_sipm - i_35v_mean) / i_35v_mean
		i_35v_pull_array.append(i_35v_pull)	
	
	vbd_pull_mean = np.mean(vbd_pull_array)
	snrpass_vbd_mean.append(vbd_pull_mean)
	vbd_pull_max = np.max(vbd_pull_array)
	snrpass_vbd_max.append(vbd_pull_max)
	vbd_pull_div = np.std(vbd_pull_array)
	snrpass_vbd_div.append(vbd_pull_div)			

	rq_pull_mean = np.mean(rq_pull_array)
	snrpass_rq_mean.append(rq_pull_mean)
	rq_pull_max = np.max(rq_pull_array)
	snrpass_rq_max.append(rq_pull_max)
	rq_pull_div = np.std(rq_pull_array)
	snrpass_rq_div.append(rq_pull_div)

	chi2_pull_mean = np.mean(chi2_pull_array)
	snrpass_chi2_mean.append(chi2_pull_mean)
	chi2_pull_max = np.max(chi2_pull_array)
	snrpass_chi2_max.append(chi2_pull_max)
	chi2_pull_div = np.std(chi2_pull_array)
	snrpass_chi2_div.append(chi2_pull_div)

	i_20v_pull_mean = np.mean(i_20v_pull_array)
	snrpass_i_20v_mean.append(i_20v_pull_mean)
	i_20v_pull_max = np.max(i_20v_pull_array)
	snrpass_i_20v_max.append(i_20v_pull_max)
	i_20v_pull_div = np.std(i_20v_pull_array)
	snrpass_i_20v_div.append(i_20v_pull_div)

	i_25v_pull_mean = np.mean(i_25v_pull_array)
	snrpass_i_25v_mean.append(i_25v_pull_mean)
	i_25v_pull_max = np.max(i_25v_pull_array)
	snrpass_i_25v_max.append(i_25v_pull_max)
	i_25v_pull_div = np.std(i_25v_pull_array)
	snrpass_i_25v_div.append(i_25v_pull_div)	
	
	i_35v_pull_mean = np.mean(i_35v_pull_array)
	snrpass_i_35v_mean.append(i_35v_pull_mean)
	i_35v_pull_max = np.max(i_35v_pull_array)
	snrpass_i_35v_max.append(i_35v_pull_max)
	i_35v_pull_div = np.std(i_35v_pull_array)
	snrpass_i_35v_div.append(i_35v_pull_div)

snrfail_vbd_mean = []
snrfail_vbd_max = []
snrfail_vbd_div = []

snrfail_rq_mean = []
snrfail_rq_max = []
snrfail_rq_div = []

snrfail_chi2_mean = []
snrfail_chi2_max = []
snrfail_chi2_div = []

snrfail_i_20v_mean = []
snrfail_i_20v_max = []
snrfail_i_20v_div = []	

snrfail_i_25v_mean = []
snrfail_i_25v_max = []
snrfail_i_25v_div = []

snrfail_i_35v_mean = []
snrfail_i_35v_max = []
snrfail_i_35v_div = []

for index, row in failedapa.iterrows():
        qrcode = row['QR code']
        vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data

        vbd_pull_array = []
        rq_pull_array = []
        chi2_pull_array = []
        i_20v_pull_array = []
        i_25v_pull_array = []
        i_35v_pull_array = []

        for sipm_id in range(1,25):
                sipm_data = dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1]

                vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1]
                vbd_pull = (vbd_sipm - vbd_mean) / vbd_mean
                vbd_pull_array.append(vbd_pull)

                rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1]
                rq_pull = (rq_sipm - rq_mean) / rq_mean
                rq_pull_array.append(rq_pull)

                chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
                chi2_pull = (chi2_sipm - chi2_mean) / chi2_mean
                chi2_pull_array.append(chi2_pull)

                i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1]
                i_20v_pull = (i_20v_sipm - i_20v_mean) / i_20v_mean
                i_20v_pull_array.append(i_20v_pull)	

                i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1]
                i_25v_pull = (i_25v_sipm - i_25v_mean) / i_25v_mean
                i_25v_pull_array.append(i_25v_pull)

                i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1]
                i_35v_pull = (i_35v_sipm - i_35v_mean) / i_35v_mean
                i_35v_pull_array.append(i_35v_pull)

        vbd_pull_mean = np.mean(vbd_pull_array)
        snrfail_vbd_mean.append(vbd_pull_mean)
        vbd_pull_max = np.max(vbd_pull_array)
        snrfail_vbd_max.append(vbd_pull_max)
        vbd_pull_div = np.std(vbd_pull_array)
        snrfail_vbd_div.append(vbd_pull_div)

        rq_pull_mean = np.mean(rq_pull_array)
        snrfail_rq_mean.append(rq_pull_mean)
        rq_pull_max = np.max(rq_pull_array)
        snrfail_rq_max.append(rq_pull_max)
        rq_pull_div = np.std(rq_pull_array)
        snrfail_rq_div.append(rq_pull_div)

        chi2_pull_mean = np.mean(chi2_pull_array)
        snrfail_chi2_mean.append(chi2_pull_mean)
        chi2_pull_max = np.max(chi2_pull_array)
        snrfail_chi2_max.append(chi2_pull_max)
        chi2_pull_div = np.std(chi2_pull_array)
        snrfail_chi2_div.append(chi2_pull_div)

        i_20v_pull_mean = np.mean(i_20v_pull_array)
        snrfail_i_20v_mean.append(i_20v_pull_mean)
        i_20v_pull_max = np.max(i_20v_pull_array)
        snrfail_i_20v_max.append(i_20v_pull_max)
        i_20v_pull_div = np.std(i_20v_pull_array)
        snrfail_i_20v_div.append(i_20v_pull_div)

        i_25v_pull_mean = np.mean(i_25v_pull_array)
        snrfail_i_25v_mean.append(i_25v_pull_mean)
        i_25v_pull_max = np.max(i_25v_pull_array)
        snrfail_i_25v_max.append(i_25v_pull_max)
        i_25v_pull_div = np.std(i_25v_pull_array)
        snrfail_i_25v_div.append(i_25v_pull_div)

        i_35v_pull_mean = np.mean(i_35v_pull_array)
        snrfail_i_35v_mean.append(i_35v_pull_mean)
        i_35v_pull_max = np.max(i_35v_pull_array)
        snrfail_i_35v_max.append(i_35v_pull_max)
        i_35v_pull_div = np.std(i_35v_pull_array)
        snrfail_i_35v_div.append(i_35v_pull_div)


fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_vbd_mean)), snrpass_vbd_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_vbd_max)), snrpass_vbd_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_vbd_div)), snrpass_vbd_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_vbd_mean)), snrfail_vbd_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_vbd_max)), snrfail_vbd_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_vbd_div)), snrfail_vbd_div, color='red')


ax.set_title('Comparing vbd pull values for Good and Bad apa values')
ax.set_ylabel('vbd Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed vbd mean', 'Failed vbd mean', 'Passed vbd max', 'Failed vbd max', 'Passed vbd div.', 'Failed vbd div.'])


fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_rq_mean)), snrpass_rq_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_rq_max)), snrpass_rq_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_rq_div)), snrpass_rq_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_rq_mean)), snrfail_rq_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_rq_max)), snrfail_rq_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_rq_div)), snrfail_rq_div, color='red')


ax.set_title('Comparing rq pull values for Good and Bad apa values')
ax.set_ylabel('rq Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed rq mean', 'Failed rq mean', 'Passed rq max', 'Failed rq max', 'Passed rq div.', 'Failed rq div.'])




fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_chi2_mean)), snrpass_chi2_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_chi2_max)), snrpass_chi2_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_chi2_div)), snrpass_chi2_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_chi2_mean)), snrfail_chi2_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_chi2_max)), snrfail_chi2_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_chi2_div)), snrfail_chi2_div, color='red')


ax.set_title('Comparing chi2 pull values for Good and Bad apa values')
ax.set_ylabel('chi2 Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed chi2 mean', 'Failed chi2 mean', 'Passed chi2 max', 'Failed chi2 max', 'Passed chi2 div.', 'Failed chi2 div.'])




fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_i_20v_mean)), snrpass_i_20v_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_i_20v_max)), snrpass_i_20v_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_i_20v_div)), snrpass_i_20v_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_i_20v_mean)), snrfail_i_20v_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_i_20v_max)), snrfail_i_20v_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_i_20v_div)), snrfail_i_20v_div, color='red')


ax.set_title('Comparing i_20v pull values for Good and Bad apa values')
ax.set_ylabel('i_20v Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed i_20v mean', 'Failed i_20v mean', 'Passed i_20v max', 'Failed i_20v max', 'Passed i_20v div.', 'Failed i_20v div.'])




fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_i_25v_mean)), snrpass_i_25v_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_i_25v_max)), snrpass_i_25v_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_i_25v_div)), snrpass_i_25v_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_i_25v_mean)), snrfail_i_25v_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_i_25v_max)), snrfail_i_25v_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_i_25v_div)), snrfail_i_25v_div, color='red')


ax.set_title('Comparing i_25v pull values for Good and Bad apa values')
ax.set_ylabel('i_25v Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed i_25v mean', 'Failed i_25v mean', 'Passed i_25v max', 'Failed i_25v max', 'Passed i_25v div.', 'Failed i_25v div.'])


fig, ax = plt.subplots()

ax.scatter(np.repeat(0, len(snrpass_i_35v_mean)), snrpass_i_35v_mean, color = 'blue')
ax.scatter(np.repeat(2, len(snrpass_i_35v_max)), snrpass_i_35v_max, color='blue')
ax.scatter(np.repeat(4, len(snrpass_i_35v_div)), snrpass_i_35v_div, color='blue')
ax.scatter(np.repeat(1, len(snrfail_i_35v_mean)), snrfail_i_35v_mean, color='red')
ax.scatter(np.repeat(3, len(snrfail_i_35v_max)), snrfail_i_35v_max, color='red')
ax.scatter(np.repeat(5, len(snrfail_i_35v_div)), snrfail_i_35v_div, color='red')


ax.set_title('Comparing i_35v pull values for Good and Bad apa values')
ax.set_ylabel('i_35v Pull')
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels(['Passed i_35v mean', 'Failed i_35v mean', 'Passed i_35v max', 'Failed i_35v max', 'Passed i_35v div.', 'Failed i_35v div.'])     

plt.show()

