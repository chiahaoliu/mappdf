"""module to demonstrate the workflow"""
import os
import numpy as np
import pandas as pd

def load_chi(lib_dir):
    """method to load chi files from lib_dir"""
    chi_fn_list = sorted([f for f in os.listdir(lib_dir) if f.endswith('.chi')])
    chi_array = []
    Q_array = []
    for chi in chi_fn_list:
        fn = os.path.join(lib_dir, chi)
        try:
            array = np.loadtxt(fn).T # pyFAI
        except:
            array = np.loadtxt(fn, skiprows=4).T # fit2D
        Q, Iq = array
        chi_array.append(Iq)
        Q_array.append(Q)
    chi_array = np.asarray(chi_array)
    Q_array = np.asarray(Q_array)
    chi_dim = chi_array.shape
    Q_dim = Q_array.shape
    # just to reproduce, dont have to save q for each of raw
    print("INFO: load {} by {} array"
          .format(Q_array.shape, chi_array.shape))
    return chi_fn_list, Q_array, chi_array


# lookup table
_df = pd.read_csv('example/EO75A_soh_1_21_17_morning.txt')

exclude_col = ['#number', 'time', 'pe1_stats1_total', 'diff_x_user_setpoint',
               'diff_y_user_setpoint', 'pe1_image']
colum_mask = [col for col in _df.columns if col not in exclude_col]
df = _df[colum_mask].copy()  # the main df to work on

# list of file name
lib_dir = 'example/fit2d_raster/'
Iq_name_list, Q_list, Iq_list = load_chi(lib_dir)

df['basename'] = pd.Series(Iq_name_list)
#Iq_df = pd.DataFrame(Iq_list)
#df['Q'] = pd.Series(Q_list)
