from ds20kdb import interface;
dbi = interface.Database();


import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

vbd = dbi.get('sipm_test',sipm_qc_id=9).data.vbd
vbd_mean = vbd.mean()
vbd_sigma = vbd.std()

rq = dbi.get('sipm_test', sipm_qc_id=11).data.rq
rq = rq[(rq >= 0) & (rq <= 100)]
rq_mean = rq.mean()
rq_sigma = rq.std()

chi2 = dbi.get('sipm_test', sipm_qc_id=11).data.chi2_shape
chi2_f = chi2[(chi2 <= 25)]
chi2_mean = chi2_f.mean()
chi2_sigma = chi2_f.std()    

i_20v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_20v
i_20v_f = i_20v[(i_20v <= 60e-12)]
i_20v_mean = i_20v_f.mean()
i_20v_sigma = i_20v_f.std()

i_25v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_25v
i_25v_f = i_25v[(i_25v <= 70e-12)]
i_25v_mean = i_25v_f.mean()
i_25v_sigma = i_25v_f.std()

i_35v = dbi.get('sipm_test', sipm_qc_id=11).data.i_at_35v
i_35v_f = i_35v[(5e-11 <= i_35v)]
i_35v_mean = i_35v_f.mean()
i_35v_sigma = i_35v_f.std()

def calculate_pull_stats(pulls):
	average_pull = np.mean(pulls)
	max_pull = np.max(pulls)
	dispersion = np.std(pulls)
	return average_pull, max_pull, dispersion

def analyse_qrcodes(qrcodes):
	dbi = interface.Database()
	all_pulls = []
	for qrcode in qrcodes:
		vtile_pull_stats = []
		vtile_ID=dbi.get_vtile_pid_from_qrcode(qrcode).data


		args = parse_args()
		dbi = interface.Database()
		qrcodes= args.qrcodes
	
		vtile_ID=dbi.get_vtile_pid_from_qrcode(qrcode).data
	
		results_df = pd.DataFrame(columns=['SIPM_ID', 'vbd_pull', 'rq_pull', 'chi2_pull', 'i_20v_pull', 'i_25v_pull', 'i_35v_pull', 'pull'])
	
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
			i_25v_pull =  abs((i_25v_sipm - i_25v_mean) / i_25v_mean)
			i_35v_pull =  abs((i_35v_sipm - i_35v_mean) / i_35v_mean)

			pull = abs((vbd_pull + rq_pull + chi2_pull + i_20v_pull + i_25v_pull + i_35v_pull)/6)
		
			pulls.append(pull)

			results_df = results_df.append({
				'SIPM_ID': sipm_id,
				'vbd_pull': vbd_pull,
				'rq_pull': rq_pull,
				'chi2_pull': chi2_pull,
				'i_20v_pull': i_20v_pull,
				'i_25v_pull': i_25v_pull,
				'i_35v_pull': i_35v_pull,
				'pull': pull
			}, ignore_index=True)
	
		pull_array = np.array(pulls)


		# creating sipm graphic	

		pull_sipm_array_reshaped = pull_array.reshape(4,6)
	
		# to get matrix in desired order, it needs to be flipped, and then transposed

		pull_sipm_flippedud = np.flipud(pull_sipm_array_reshaped)
	
		pull_sipm_array = pull_sipm_flippedud.T	
				
		cmap = plt.get_cmap('coolwarm')

		plt.imshow(pull_sipm_array, cmap=cmap, interpolation='nearest', aspect='auto')	
	
		plt.colorbar()

		for i in range(pull_sipm_array.shape[0]):
			for j in range(pull_sipm_array.shape[1]):
				plt.text(j, i, f'{pull_sipm_array[i, j]:.2f}', ha='center', va='center', color='black')
	
		plt.title(f'Pull values of SiPMs of vTile {vtile_ID}')
	

		plt.show()

def plot_comparison(all_pulls, qrcodes):
	averages = [stats[0] for stats in all_pulls]
	max_pulls = [stats[1] for stats in all_pulls]
	dispersions = [stats[2] for stats in all_pulls]

	x = np.arange(len(qrcodes))

def parse_args():
	parser = argparse.ArgumentParser(description='Pass/Fail System')
	parser.add_argument('--qrcodes', nargs='+', type=str, required=True, help='List of QR codes for analysis')
	return parser.parse_args()

def main():
	args = parse_args()
	analyse_qrcodes(args.qrcodes)

if __name__ == "__main__":
    main()





