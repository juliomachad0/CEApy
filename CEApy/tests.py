import logging as log
from CEApy import CEA
import matplotlib.pyplot as plt

oxidante = [['N2O', 100, 298.15]]
fuel = [['CH3NO2(L)', 100, 298.15]]


def if_string_to_lower(column_names):
    if type(column_names) is list:
        for i in column_names:
            if type(i) is str:
                pass
            else:
                log.error('CEA: {} item is not a string\n'.format(i))
                return
        column_names = [s.replace(s, s.lower()) for s in column_names]
    return column_names


aeat = [200]
pressure = [10]
of = [0.5, 0.75, 1, 2, 3, 4]
L22 = CEA()
L22.settings()
L22.input_propellants(oxid=oxidante, fuel=fuel)
L22.input_parameters(chamber_pressure=pressure, sup_aeat=aeat, of_ratio=of)
L22.output_parameters(['cf', 'isp', 'gam', 'pipe', 'o/f', 'ivac'])
L22.run()
df = L22.get_results('all', 'exit')

if df is not None:
    df['isp'] = df['isp']/9.8
    df['ivac'] = df['ivac']/9.8
    print(df.head())

plt.plot(df['gam'], df['isp'])
print(df['gam'])
plt.show()
