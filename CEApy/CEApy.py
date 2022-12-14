import os
import pandas as pd
import logging as log
from time import sleep
log.basicConfig(level=log.INFO)


class CEA:
    def __init__(self, name="CEA_Analysis"):
        # arquivo e nome do estudo
        self.caminho_raiz = str(os.path.dirname(__file__))
        self.case = str(name)
        self.file_name = self.case + '.inp'
        self.input_text = []  # lista de input CEA
        self.input_text_string = ''  # string de input CEA
        # parametros de configuração
        self.combustion_temp = 3800
        self.nfz_cond = 1
        self.nfz = 3
        self.short = 0
        self.intermediate = 0
        self.transport = 0
        self.nominal_thrust = None  # newton
        self.equi = 1
        self.chamber_pressure = []  # bar
        # propelentes
        self.oxids = []
        self.fuels = []
        # variaveis
        self.sup_aeat_cond = 0  # 0 nao considera, 1 considera
        self.sup_aeat = []
        self.sub_aeat_cond = 0  # 0 nao considera, 1 considera
        self.sub_aeat = []
        self.pipe_cond = 0  # 0 nao considera, 1 considera
        self.pipe = []
        self.of_ratio_cond = 0  # 0 nao considera, 1 considera
        self.of_ratio = []
        # plots
        self.plot_p = 0
        self.plot_t = 0
        self.plot_cp = 0
        self.plot_mw = 0
        self.plot_mach = 0
        self.plot_isp = 0
        self.plot_ivac = 0
        self.plot_vis = 0
        self.plot_cond = 0
        self.plot_pran = 0
        self.plot_cf = 0
        self.plot_h = 0
        self.plot_r_eq_ratio = 0
        self.plot_phi_eq_ratio = 0
        self.plot_of_ratio = 0
        self.output_aeat_variable = 0

    def search_specie(self, words):
        os.chdir(self.caminho_raiz)
        thermo = open('cea-exec/thermo_convertido.txt', 'r')
        linhas = thermo.readlines()
        cont = 1
        for linha in linhas:
            if words in linha:
                print('resultado {}: '.format(cont) + linha)
                cont = cont + 1
        if cont == 1:
            print('NO ONE SPECIE HAS BEEN FOUND\n')

    def show_all_species(self):
        os.chdir(self.caminho_raiz)
        thermo = open('cea-exec/thermo_convertido.txt', 'r')
        linhas = thermo.readlines()
        cont = 1
        print('All THE SPECIES AVAILABLE IN CEA\nTHERMODYNAMICAL DATABASE:\n')
        for linha in linhas:
            print('specie {}: '.format(cont) + linha)
            cont = cont + 1

    def input_oxids(self, oxid):
        self.oxids = oxid

    def input_fuels(self, fuel):
        self.fuels = fuel

    def input_frozen_station(self, condicao, freezing_point):
        condicao = str(condicao)
        if condicao.lower() == 'sim':
            self.nfz_cond = 1
            if (freezing_point == 'combustor') or (freezing_point == 1):
                self.nfz = 1
            if (freezing_point == 'throat') or (freezing_point == 2):
                self.nfz = 2
            if (freezing_point == 'exit') or (freezing_point == 3):
                self.nfz = 3
        elif (condicao.lower() == 'nao') or (condicao.lower() == 'não'):
            self.nfz_cond = 0

    def input_equi_condition(self, condicao):
        condicao = str(condicao)
        if condicao.lower() == 'sim':
            self.equi = 1
        elif (condicao.lower() == 'nao') or (condicao.lower() == 'não'):
            self.equi = 0

    def enable_short_output(self):
        self.short = 1

    def enable_transport_prop(self):
        self.transport = 1

    def show_input_file(self):
        print(self.input_text_string)

    # variables
    def input_pressure_chamber(self, pressure):
        self.chamber_pressure = pressure

    def input_pipe(self, pipe):
        self.pipe_cond = 1
        self.pipe = pipe

    def input_sub_aeat(self, sub_aeat):
        self.sub_aeat_cond = 1
        self.sub_aeat = sub_aeat

    def input_sup_aeat(self, sup_aeat):
        self.sup_aeat_cond = 1
        self.sup_aeat = sup_aeat

    def input_of_ratio(self, of_ratio):
        self.of_ratio_cond = 1
        self.of_ratio = of_ratio

    def input_combustion_temp(self, comb_temp):
        self.combustion_temp = comb_temp

    # output
    def output_pressure_combustion(self):
        self.plot_p = 1

    def output_temp_combustion(self):
        self.plot_t = 1

    def output_temp_heat_capacity(self):
        self.plot_cp = 1

    def output_molecular_weight(self):
        self.plot_mw = 1

    def output_mach(self):
        self.plot_mach = 1

    def output_isp(self):
        self.plot_isp = 1

    def output_isp_vacuum(self):
        self.plot_ivac = 1

    def output_viscosity(self):
        self.plot_vis = 1

    def output_thermal_condutivity(self):
        self.plot_cond = 1

    def output_prandtl_number(self):
        self.plot_pran = 1

    def output_thrust_coef(self):
        self.plot_cf = 1

    def output_entalphy(self):
        self.plot_h = 1

    def output_chemical_equivalence_ratio(self):
        self.plot_r_eq_ratio = 1

    def output_phi_equivalence_ratios_f_to_o(self):
        self.plot_phi_eq_ratio = 1

    def output_of_ratio(self):
        self.plot_of_ratio = 1

    def output_aeat(self):
        self.output_aeat_variable = 1

    def all_output_available(self):
        self.plot_p = 1
        self.plot_t = 1
        self.plot_cp = 1
        self.plot_mw = 1
        self.plot_mach = 1
        self.plot_isp = 1
        self.plot_ivac = 1
        self.plot_vis = 1
        self.plot_cond = 1
        self.plot_pran = 1
        self.plot_cf = 1
        self.plot_h = 1
        self.plot_r_eq_ratio = 1
        self.plot_phi_eq_ratio = 1
        self.plot_of_ratio = 1

    def run(self):
        # **** CRIANDO TEXTO INPUT ****
        # primeira linha
        primeira_linha = 'problem case={}\n'.format(self.case)
        # segunda linha
        segunda_linha = '   rocket'
        if self.equi == 1:
            segunda_linha = segunda_linha + ' equilibrium'
        if self.nfz_cond == 1:
            segunda_linha = segunda_linha + ' frozen nfz={}'.format(self.nfz)
        if self.combustion_temp != 3800:
            segunda_linha = segunda_linha + ' tcest,k={}'.format(self.combustion_temp)
        segunda_linha = segunda_linha + '\n'
        self.input_text.append(primeira_linha)
        self.input_text.append(segunda_linha)
        # adicionando pressao
        pressure = ' p,bar='
        for i in self.chamber_pressure:
            pressure = pressure + ('{},'.format(i))
        self.input_text.append(pressure + '\n')
        # adidcionando pipe
        if self.pipe_cond == 1:
            pipe = ' pi/p='
            for i in self.pipe:
                pipe = pipe + ('{},'.format(i))
            self.input_text.append(pipe + '\n')

        # adicionando aeat subsonic
        if self.sub_aeat_cond == 1:
            aeatsub = ' sub,ae/at='
            for i in self.sub_aeat:
                aeatsub = aeatsub + ('{},'.format(i))
            # self.input_text.append(aeatsub + '\n')

        # ADICIONANDO aeat supersonic
        if self.sup_aeat_cond == 1:
            aeatsup = ' sup,ae/at='
            for i in self.sup_aeat:
                aeatsup = aeatsup + ('{},'.format(i))
            self.input_text.append(aeatsup + '\n')
        # adicionando o/f
        if self.of_ratio_cond == 1:
            of_ratio = ' o/f='
            for i in self.of_ratio:
                of_ratio = of_ratio + ('{},'.format(i))
            self.input_text.append(of_ratio + '\n')
        # react
        self.input_text.append('react\n')
        # COMBUSTIVEL
        for i in self.fuels:
            self.input_text.append(' fuel={} wt={} t,k={}\n'.format(i[0], i[1], i[2]))
        # Oxidantes
        for i in self.oxids:
            self.input_text.append(' oxid={} wt={} t,k={}\n'.format(i[0], i[1], i[2]))
        # output
        output = 'output siunits'
        if self.short == 1:
            output = output + ' short'
        if self.transport == 1:
            output = output + ' transpot'
        self.input_text.append(output + '\n')
        # plot
        plot = '    plot'
        if self.plot_p == 1:
            plot = plot + ' p'
        if self.plot_t == 1:
            plot = plot + ' t'
        if self.plot_cp == 1:
            plot = plot + ' cp'
        if self.plot_mw == 1:
            plot = plot + ' mw'
        if self.plot_mach == 1:
            plot = plot + ' mach'
        if self.plot_isp == 1:
            plot = plot + ' isp'
        if self.plot_ivac == 1:
            plot = plot + ' ivac'
        if self.plot_vis == 1:
            plot = plot + ' vis'
        if self.plot_cond == 1:
            plot = plot + ' cond'
        if self.plot_pran == 1:
            plot = plot + ' pran'
        if self.plot_cf == 1:
            plot = plot + ' cf'
        if self.plot_h == 1:
            plot = plot + ' h'
        if self.plot_r_eq_ratio == 1:
            plot = plot + ' r,eq.ratio'
        if self.plot_phi_eq_ratio == 1:
            plot = plot + ' phi,eq.ratio'
        if self.plot_of_ratio == 1:
            plot = plot + ' o/f'
        if self.output_aeat_variable == 1:
            plot = plot + ' aeat'
        self.input_text.append(plot + '\n')
        # end
        self.input_text.append('end\n')

        # **** GRAVANDO NO ARQUIVO E EXECUTANTO ****
        # configurando arquivo de input
        os.chdir(self.caminho_raiz)
        with open('cea-exec/cea_python_input.txt', 'w') as inputbat:
            inputbat.write(self.case)
        # excluindo arquivos anteriores
        if os.path.exists('cea-exec/{}.inp'.format(self.case)):
            os.remove('cea-exec/{}.inp'.format(self.case))
            # arquivos .inp
        if os.path.exists('cea-exec/{}.out'.format(self.case)):
            os.remove('cea-exec/{}.out'.format(self.case))
            # arquivos .out
        if os.path.exists('cea-exec/{}.plt'.format(self.case)):
            os.remove('cea-exec/{}.plt'.format(self.case))
            # arquivos .plt
        if os.path.exists('cea-exec/{}.csv'.format(self.case)):
            os.remove('cea-exec/{}.csv'.format(self.case))
            # arquivos .csv
        # gravando no arquivo .inp
        arquivo = open('cea-exec/{}'.format(self.file_name), 'w')
        for i in self.input_text:
            self.input_text_string = self.input_text_string + str(i) + '\n'
        arquivo.write(self.input_text_string)
        arquivo.close()
        # executando bat file
        os.chdir(self.caminho_raiz+'/cea-exec/')
        os.startfile("cea_python.vbs")
        os.chdir(self.caminho_raiz)
        # limpando variaveis
        self.input_text = []
        self.input_text_string = ''
        sleep(1.5)

    def vizualize_output_file(self):
        os.chdir(self.caminho_raiz)
        arquivo = open('cea-exec/{}.out'.format(self.case), 'r')
        arquivo = arquivo.readlines()
        for i in arquivo:
            print(i)

    def get_results(self, column_names, condition):
        if type(condition) is str:
            condition = str(condition).lower()
        if type(column_names) is str:
            column_names = str(column_names).lower()
        # getting data.csv
        os.chdir(self.caminho_raiz)
        df = pd.read_csv('cea-exec/{}.csv'.format(self.case))
        # rename properly
        for i in df.columns:
            df.rename(columns={i: str(i).strip()}, inplace=True)

        # if all columns with all data are requested
        if (column_names == 'all') and (condition == 'all'):
            return df
        # if all columns with specific condition are requested
        elif (column_names == 'all') and (condition != 'all'):
            if (condition == 'combustor') or (condition == 1):
                return data_exit_condition(df, 0)
            elif (condition == 'throat') or (condition == 2):
                return data_exit_condition(df, 1)
            elif (condition == 'exit') or (condition == 3):
                if condition == 'exit':
                    return data_exit_condition(df, 2)
                else:
                    return data_exit_condition(df, condition-1)
            else:
                log.error("\nCondition not informed properly, options:\n"
                          "All, ALL, all, exit, combustor, throat, 1, 2, 3 ...\n")
                return
        # if specific columns are requested with specific condition
        elif type(column_names) is list:
            # building desired df
            vectors_list_names = []
            for i in column_names:
                if i in df.columns:
                    for j in df.columns:
                        if i == j:
                            vectors_list_names.append(j)
                else:
                    log.error("\n{} is not in results\n".format(i))
                    print('column names available in results: {}\n'.format(df.columns))
                    return
            new_df = df[vectors_list_names]

            if (condition == 'combustor') or (condition == 1):
                return data_exit_condition(new_df, 0)
            elif (condition == 'throat') or (condition == 2):
                return data_exit_condition(new_df, 1)
            elif (condition == 'exit') or (condition == 3):
                if condition == 'exit':
                    return data_exit_condition(new_df, 2)
                else:
                    return data_exit_condition(new_df, condition-1)
            elif condition == 'all':
                return new_df
            else:
                log.error("\nCondition not informed properly, options:\n"
                          "All, ALL, all, exit, combustor, throat, 1, 2, 3 ...\n")
                return
        else:
            log.error("Column names are not informed properly, options:\n"
                      "All, ALL, all or list with specific names of columns\n")
            return


def data_exit_condition(df, cond):
    df_new = None
    c = 0
    for cln in df.columns:
        cl = []
        for j in range(cond, len(df[cln]), 3):
            cl.append(df[cln][j])
        if c == 0:
            df_new = pd.DataFrame(cl, columns=[cln])
        else:
            df_new[cln] = cl
        c = c + 1
    return df_new
