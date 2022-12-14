from CEApy import CEA
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

def data_exit_condition(df,cond):
    df_new = None
    c = 0
    for cln in df.columns:
        cl = []
        for j in range(cond, len(df[cln]), 3):
            cl.append(df[cln][j])
        if c == 0:
            df_new = pd.DataFrame(cl, columns=[cln])
        elif c != 0:
            df_new[cln] = cl
        c = c + 1
    return df_new


def plot_curve(x, y, leg_x, leg_y, tit, curva):
    plt.plot(x, y, 'o--', label=curva)
    plt.legend()
    plt.xlabel(leg_x)
    plt.ylabel(leg_y)
    plt.title(leg_x + ' X ' + leg_y+tit)


# INICIANDO ANALISE
oxidante = [['N2O', 100, 300]]  # OXIDO NITROSO
aeat = [100, 150, 170, 200, 220, 250]
of = [0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
pressure = [10]  # bar
# L22 Nitrometano
L22_nitro = CEA('L22_analise_nitrometano')
fuel_nitro = [['CH3NO2(L)', 100, 298.15]]
L22_nitro.input_oxids(oxidante)
L22_nitro.input_fuels(fuel_nitro)
L22_nitro.input_of_ratio(of)
L22_nitro.input_pressure_chamber(pressure)
L22_nitro.input_frozen_station('sim', 'exit')
L22_nitro.enable_short_output()
L22_nitro.enable_transport_prop()
L22_nitro.output_isp()
L22_nitro.output_thrust_coef()
L22_nitro.output_of_ratio()
L22_nitro.output_aeat()

L22_nitro.input_sup_aeat([200])
L22_nitro.run()
aeat_isp = L22_nitro.get_results(['cf', 'o/f'], 'throat')

# print('curva aeat x isp: \n', aeat_isp)


"""
# ANALISE NITROMETANO
df_nitro_100 = None
df_nitro_150 = None
df_nitro_170 = None
df_nitro_200 = None
df_nitro_220 = None
df_nitro_250 = None
cont = 0
for i in aeat:
    print('teste {}'.format(cont))
    L22_nitro.input_sup_aeat([i])
    L22_nitro.run()
    sleep(1)
    df_nitro = L22_nitro.get_results()
    if cont == 0:
        df_nitro_100 = data_exit_condition(df_nitro)
        print(df_nitro_100["isp"][0])
    if cont == 1:
        df_nitro_150 = data_exit_condition(df_nitro)
    if cont == 2:
        df_nitro_170 = data_exit_condition(df_nitro)
    if cont == 3:
        df_nitro_200 = data_exit_condition(df_nitro)
    if cont == 4:
        df_nitro_220 = data_exit_condition(df_nitro)
    if cont == 5:
        df_nitro_250 = data_exit_condition(df_nitro)
    print('iter: {}, value: {}\n'.format(cont, i))
    cont = cont + 1
"""
"""
# ISP
df_nitro_100['isp'] = df_nitro_100['isp'] / 9.81
plot_curve(df_nitro_100['o/f'], df_nitro_100['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=100')

df_nitro_150['isp'] = df_nitro_150['isp'] / 9.81
plot_curve(df_nitro_150['o/f'], df_nitro_150['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=150')

df_nitro_170['isp'] = df_nitro_170['isp'] / 9.81
plot_curve(df_nitro_170['o/f'], df_nitro_170['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=170')

df_nitro_200['isp'] = df_nitro_200['isp'] / 9.81
plot_curve(df_nitro_200['o/f'], df_nitro_200['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=200')

df_nitro_220['isp'] = df_nitro_220['isp'] / 9.81
plot_curve(df_nitro_220['o/f'], df_nitro_220['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=220')

df_nitro_250['isp'] = df_nitro_250['isp'] / 9.81
plot_curve(df_nitro_250['o/f'], df_nitro_250['isp'],
           'O/F', 'Isp (s)',
           ' Nitrometano',
           'aeat=250')
plt.show()
"""
# L22_nitro.vizualize_output_file()
"""
CEA().search_specie('N2O')
CEA().show_all_species()
"""