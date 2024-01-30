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

# a = average, m = max, d = divergence

gvbd_a = []
gvbd_m = []
gvbd_d = []

grq_a = []
grq_m = []
grq_d = []

gchi2_a = []
gchi2_m = []
gchi2_d = []

g20_a = []
g20_m = []
g20_d = []

g25_a = []
g25_m = []
g25_d = []

g35_a = []
g35_m = []
g35_d = []

for index, row in good_tiles.iterrows():	
	qrcode = row['QR code']
	vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data	

	pulls = []
	vbdpulls = []
	rqpulls = []
	chi2pulls = []
	pulls20 = []
	pulls25 = []
	pulls35 = []	
	for sipm_id in range(1,25):
	

						
		sipm_data = dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1] 
		vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1] 
		rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1] 
		chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
		i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1] 
		i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1] 
		i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1] 
  

		vbd_pull = abs((vbd_sipm - vbd_mean) / vbd_mean)
		vbdpulls.append(vbd_pull)
		rq_pull =  abs((rq_sipm - rq_mean) / rq_mean)
		rqpulls.append(rq_pull) 
		chi2_pull =  abs((chi2_sipm - chi2_mean) / chi2_mean) 
		chi2pulls.append(chi2_pull)
		i_20v_pull =  abs((i_20v_sipm - i_20v_mean) / i_20v_mean) 
		pulls20.append(i_20v_pull)
		i_25v_pull =  abs((i_25v_sipm - i_25v_mean) / i_25v_mean) 
		pulls25.append(i_25v_pull)
		i_35v_pull =  abs((i_35v_sipm - i_35v_mean) / i_35v_mean) 
		pulls35.append(i_35v_pull)
		
		pull = abs((vbd_pull + rq_pull + chi2_pull + i_20v_pull + i_25v_pull + i_35v_pull)/6) 
		pulls.append(pull)
	
	pull_average = np.mean(pulls)
	good_average.append(pull_average)		
	pull_max = np.max(pulls)
	good_max.append(pull_max)
	pull_std = np.std(pulls)
	good_std.append(pull_std)

	vbda = np.mean(vbdpulls)
	gvbd_a.append(vbda)
	vbdm = np.max(vbdpulls)
	gvbd_m.append(vbdm)
	vbdd = np.std(vbdpulls)
	gvbd_d.append(vbdd)

	rqa = np.mean(rqpulls)
	grq_a.append(rqa)
	rqm = np.max(rqpulls)
	grq_m.append(rqm)
	rqd = np.std(rqpulls)
	grq_d.append(rqd)		

	chi2a = np.mean(chi2pulls)
	gchi2_a.append(chi2a)
	chi2m = np.max(chi2pulls)
	gchi2_m.append(chi2m)
	chi2d = np.std(chi2pulls)
	gchi2_d.append(chi2d)

	a20 = np.mean(pulls20)
	g20_a.append(a20)
	m20 = np.max(pulls20)
	g20_m.append(m20)
	d20 = np.std(pulls20)
	g20_d.append(d20)

	a25 = np.mean(pulls25)
	g25_a.append(a25)
	m25 = np.max(pulls25)
	g25_m.append(m25)
	d25 = np.std(pulls25)
	g25_d.append(d25)

	a35 = np.mean(pulls35)
	g35_a.append(a35)
	m35 = np.max(pulls35)
	g35_m.append(m35)
	d35 = np.std(pulls35)
	g35_d.append(d35)

bad_average = []
bad_max = []
bad_std = []

bvbd_a = []
bvbd_m = []
bvbd_d = []

brq_a = []
brq_m = []
brq_d = []

bchi2_a = []
bchi2_m = []
bchi2_d = []

b20_a = []
b20_m = []
b20_d = []

b25_a = []
b25_m = []
b25_d = []

b35_a = []
b35_m = []
b35_d = []

for index, row in bad_tiles.iterrows():
        qrcode = row['QR code']
        vtile_ID = dbi.get_vtile_pid_from_qrcode(qrcode).data

        pulls = []
        vbdpulls = []
        rqpulls = []
        chi2pulls = []
        pulls20 = []
        pulls25 = []
        pulls35 = []

        for sipm_id in range(1,25):


                sipm_data =  dbi.get('vtile', vtile_pid=vtile_ID).data[f'sipm_{sipm_id}'].iloc[-1]

                vbd_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.vbd.iloc[-1]
                rq_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.rq.iloc[-1]
                chi2_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.chi2_shape.iloc[-1]
                i_20v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_20v.iloc[-1]
                i_25v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_25v.iloc[-1]
                i_35v_sipm = dbi.get('sipm_test',sipm_id=sipm_data).data.i_at_35v.iloc[-1]

                vbd_pull = abs((vbd_sipm - vbd_mean) / vbd_mean)
                vbdpulls.append(vbd_pull)
                rq_pull =  abs((rq_sipm - rq_mean) / rq_mean)
                rqpulls.append(rq_pull)
                chi2_pull =  abs((chi2_sipm - chi2_mean) / chi2_mean)
                chi2pulls.append(chi2_pull)
                i_20v_pull =  abs((i_20v_sipm - i_20v_mean) / i_20v_mean)
                pulls20.append(i_20v_pull)
                i_25v_pull =  abs((i_25v_sipm - i_25v_mean) / i_25v_mean)
                pulls25.append(i_25v_pull)
                i_35v_pull =  abs((i_35v_sipm - i_35v_mean) / i_35v_mean)
                pulls35.append(i_35v_pull)

                pull = abs((vbd_pull + rq_pull + chi2_pull + i_20v_pull + i_25v_pull + i_35v_pull)/6)
                pulls.append(pull)

        pull_average = np.mean(pulls)
        bad_average.append(pull_average)

        pull_max = np.max(pulls)		
        bad_max.append(pull_max)

        pull_std = np.std(pulls)
        bad_std.append(pull_std)

        vbda = np.mean(vbdpulls)
        bvbd_a.append(vbda)
        vbdm = np.max(vbdpulls)
        bvbd_m.append(vbdm)
        vbdd = np.std(vbdpulls)
        bvbd_d.append(vbdd)

        rqa = np.mean(rqpulls)
        brq_a.append(rqa)
        rqm = np.max(rqpulls)
        brq_m.append(rqm)
        rqd = np.std(rqpulls)
        brq_d.append(rqd)

        chi2a = np.mean(chi2pulls)
        bchi2_a.append(chi2a)
        chi2m = np.max(chi2pulls)
        bchi2_m.append(chi2m)
        chi2d = np.std(chi2pulls)
        bchi2_d.append(chi2d)

        a20 = np.mean(pulls20)
        b20_a.append(a20)
        m20 = np.max(pulls20)
        b20_m.append(m20)
        d20 = np.std(pulls20)
        b20_d.append(d20)

        a25 = np.mean(pulls25)
        b25_a.append(a25)
        m25 = np.max(pulls25)
        b25_m.append(m25)
        d25 = np.std(pulls25)
        b25_d.append(d25)

        a35 = np.mean(pulls35)
        b35_a.append(a35)
        m35 = np.max(pulls35)
        b35_m.append(m35)
        d35 = np.std(pulls35)
        b35_d.append(d35)

#df_g_average = pd.DataFrame(good_average)
#df_g_average.to_csv('good_averages.csv', index=False)

#df_g_max = pd.DataFrame(good_max)
#df_g_max.to_csv('good_max.csv', index=False)

#df_g_std = pd.DataFrame(good_std)
#df_g_std.to_csv('good_divergence.csv', index=False)

#df_b_average = pd.DataFrame(bad_average)
#df_b_average.to_csv('bad_averages.csv', index=False)

#df_b_max = pd.DataFrame(bad_max)
#df_b_max.to_csv('bad_max.csv', index=False)

#df_b_std = pd.DataFrame(bad_std)
#df_b_std.to_csv('bad_divergence.csv', index=False)

dfvbdg = pd.DataFrame({
	'Average': gvbd_a,
	'Max': gvbd_m,
	'Divergence': gvbd_d
	})

dfvbdg.to_csv('goodvbdpulls.csv', index=False)

dfrqg = pd.DataFrame({
        'Average': grq_a,
        'Max': grq_m,
        'Divergence': grq_d
        })

dfrqg.to_csv('goodrqpulls.csv', index=False)

dfchi2g = pd.DataFrame({
        'Average': gchi2_a,
        'Max': gchi2_m,
        'Divergence': gchi2_d
        })

dfchi2g.to_csv('goodchi2pulls.csv', index=False)

df20g = pd.DataFrame({
        'Average': g20_a,
        'Max': g20_m,
        'Divergence': g20_d
        })

df20g.to_csv('good20pulls.csv', index=False)

df25g = pd.DataFrame({
        'Average': g25_a,
        'Max': g25_m,
        'Divergence': g25_d
        })

df25g.to_csv('good25pulls.csv', index=False)

df35g = pd.DataFrame({
        'Average': g35_a,
        'Max': g35_m,
        'Divergence': g35_d
        })

df35g.to_csv('good35pulls.csv', index=False)

dfvbdb = pd.DataFrame({
        'Average': bvbd_a,
        'Max': bvbd_m,
        'Divergence': bvbd_d
        })

dfvbdb.to_csv('badvbdpulls.csv', index=False)

dfrqb = pd.DataFrame({
        'Average': brq_a,
        'Max': brq_m,
        'Divergence': brq_d
        })

dfrqb.to_csv('badrqpulls.csv', index=False)

dfchi2b = pd.DataFrame({
        'Average': bchi2_a,
        'Max': bchi2_m,
        'Divergence': bchi2_d
        })

dfchi2b.to_csv('badchi2pulls.csv', index=False)

df20b = pd.DataFrame({
        'Average': b20_a,
        'Max': b20_m,
        'Divergence': b20_d
        })

df20b.to_csv('bad20vpulls.csv', index=False)

df25b = pd.DataFrame({
        'Average': b25_a,
        'Max': b25_m,
        'Divergence': b25_d
        })

df25b.to_csv('bad25vpulls.csv', index=False)

df35b = pd.DataFrame({
        'Average': b35_a,
        'Max': b35_m,
        'Divergence': b35_d
        })

df35b.to_csv('bad35vpulls.csv', index=False)
