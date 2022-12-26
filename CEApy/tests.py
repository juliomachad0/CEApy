from CEApy import CEA
import matplotlib.pyplot as plt
combustion = CEA("My_first_Analysis")
combustion.settings()
combustion.input_propellants(oxid=[['O2(L)', 100, 90.17]], fuel=[['RP-1', 100, 298.15]])
combustion.input_parameters(sup_aeat=[200], chamber_pressure=[10],
                            of_ratio=[0.5, 1, 2, 3])
combustion.output_parameters(user_outputs=['isp', 'cf', 'o/f'])
combustion.run()
df = combustion.get_results()
df['isp'] = df['isp']/9.81
print(df)
plt.plot(df['o/f'], df['isp'])
plt.title('O/F x Isp (s), sup_aeat=200, pc = 10 bar')
plt.xlabel('O/F')
plt.ylabel('Isp (s)')
plt.legend('isp')
plt.show()
strings = combustion.get_simulation_file('out')


combustion.remove_analysis_file()
