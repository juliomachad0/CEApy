import os
import pandas as pd
import logging as log
from time import sleep

log.basicConfig(level=log.INFO)


class CEA:
    def __init__(self, name="CEA_Analysis"):

        # file path and name of analysis
        self.__caminho_raiz = str(os.path.dirname(__file__))
        self.__case = str(name)  # name of analysis
        self.__file_name = self.__case + '.inp'
        self.__input_text = []  # lista de input CEA
        self.__input_text_string = ''  # string de input CEA, initial length = 0

        # setting parameters of simulation
        # setting condition to start simulation
        self.__setting_parameters_condition = 0
        # combustion chamber
        self.__nfz_cond = 1  # frozen condition
        self.__nfz = 3  # freezing point
        self.__equilibrium = 1  # equilibrium condition
        # output file, conditions
        self.__short = 0
        self.__intermediate = 0
        # transport properties, conditions
        self.__transport = 0
        # data exit, to avoid static method
        self.__df_new = None

        # PROPELLANT
        # propellants variables
        self.__propellant_v_condition = 0
        self.__oxids = []
        self.__fuels = []

        # INPUT
        # simulation input variables
        # assessing if empty or not
        self.__input_parameters_condition = 0
        # condition
        self.__chamber_pressure_cond = 0  # 0 disable, 1 enable
        self.__sub_aeat_cond = 0  # 0 disable, 1 enable
        self.__sup_aeat_cond = 0  # 0 disable, 1 enable
        self.__pipe_cond = 0  # 0 disable, 1 enable
        # ratios
        self.__of_ratio_cond = 0  # 0 disable, 1 enable
        self.__chem_ratio_cond = 0
        self.__phi_ratio_cond = 0
        self.__fbyw_ratio_cond = 0
        # values
        self.__combustion_temp = 3800  # standard temperature of CEA
        self.__chamber_pressure = []  # bar
        self.__sub_aeat = []  # subsonic expansion ratio of divergent
        self.__sup_aeat = []  # supersonic expansion ratio of divergent
        self.__pipe = []  # pressure ratio p_in/p_exit
        # ratios
        self.__of_ratio = []  # mixture ratio of propellant oxid/fuel
        self.__chem_ratio = []
        self.__phi_ratio = []
        self.__fbyw_ratio = []
        # OUTPUT
        # variables which the simulation must plot
        # assessing if empty or not
        self.__output_parameters_condition = 0
        # 0 -> disable, 1 -> enable
        self.__output_list = [
            'p', 't', 'rho', 'h', 'u', 'g', 's', 'm', 'mw', 'cp', 'gam', 'son',  # thermo prop
            'pipe', 'mach', 'aeat', 'cf', 'ivac', 'isp',  # rocket performance
            'vis', 'cond', 'condfz', 'pran',  'pranfz',  # transport properties
            '%f', 'o/f', 'phi,eq.ratio', 'r,eq.ratio']  # fuel-oxidant mixture parameters
        # thermodynamical properties
        self.__out_p = 0
        self.__out_t = 0
        self.__out_rho = 0
        self.__out_h = 0
        self.__out_u = 0
        self.__out_g = 0
        self.__out_s = 0
        self.__out_m = 0
        self.__out_mw = 0
        self.__out_cp = 0
        self.__out_gam = 0
        self.__out_son = 0
        # rocket performance
        self.__out_pipe = 0
        self.__out_mach = 0
        self.__out_aeat = 0
        self.__out_cf = 0
        self.__out_ivac = 0
        self.__out_isp = 0
        # transport properties
        self.__out_vis = 0
        self.__out_cond = 0
        self.__out_condfz = 0
        self.__out_pran = 0
        self.__out_pranfz = 0
        # fuel-oxidant mixtures
        self.__out_fbw_ratio = 0  # %f
        self.__out_chem_eq_ratio = 0  # r,eq.ratio
        self.__out_phi_eq_ratio = 0  # phi,eq.ratio
        self.__out_of_ratio = 0  # o/f

    def search_specie(self, words):
        os.chdir(self.__caminho_raiz)
        thermo = open('cea-exec/thermo_convertido.txt', 'r')
        linhas = thermo.readlines()
        cont = 0
        for linha in linhas:
            if words in linha:
                print('Result {}: '.format(cont) + linha)
                cont = cont + 1
        if cont == 0:
            log.info("CEA: Search specie method\nNO ONE {} OR SIMILAR SPECIE HAS BEEN FOUND\n")

    def show_all_species(self):
        os.chdir(self.__caminho_raiz)
        thermo = open('cea-exec/thermo_convertido.txt', 'r')
        linhas = thermo.readlines()
        cont = 1
        print('CEA: Show all species method\n'
              'All THE SPECIES AVAILABLE IN CEA\nTHERMODYNAMICAL DATABASE:\n')
        for linha in linhas:
            print('Specie {}: '.format(cont) + linha)
            cont = cont + 1

    def __search_input_propellants(self, word):
        os.chdir(self.__caminho_raiz)
        thermo = open('cea-exec/thermo_convertido.txt', 'r')
        linhas = thermo.readlines()
        cont = 0
        for i in linhas:
            if word in i:
                cont += 1
        if cont == 0:
            log.error("CEA: NO ONE {} SPECIE HAS BEEN FOUND".format(word))
            log.info("CEA: SIMILAR SPECIES FOUND: \n")
            self.search_specie(word)
            return 0
        else:
            return 1

    def input_propellants(self, oxid=None, fuel=None):
        # assessing oxid coherence
        if oxid is not None:
            for i in oxid:
                if len(i) == 3:
                    if (type(i[0]) is str) and (type(i[1]) is int or float) and (type(i[2]) is int or float):
                        pass
                    elif (type(i[0]) is str) and (type(i[1]) is int or float) and (type(i[2]) is int or float):
                        pass
                    else:
                        log.error("CEA: Input propellant method"
                                  "\nOXIDIZER - Oxid and fuel parameters must be a list inside a list, like:\n"
                                  "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one\n"
                                  "-instruction:\n"
                                  "name must be string, mass fraction and temperature must be float or int\n")
                        self.__propellant_v_condition = 0
                        return
                else:
                    log.error("CEA: Input propellant method\n"
                              "OXIDIZER -  Oxid and fuel parameters must be a list inside a list, like:\n"
                              "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one\n"
                              "- instruction:\n"
                              "name must be string, mass fraction and temperature must be float or int\n")
                    self.__propellant_v_condition = 0
                    return
            #  verifying existence of species
            for i in oxid:
                result_search = self.__search_input_propellants(i[0])
                if result_search == 0:
                    return
            #  setting oxidizer
            self.__oxids = oxid
        elif fuel is None:
            log.error("CEA:  Input propellant method\n"
                      "OXIDIZER - Both oxid and fuel parameters are empty or not a list\n"
                      "CEA: Oxid and fuel parameters must be a list inside a list, like:\n"
                      "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one"
                      "- instruction:\n"
                      "name must be string, mass fraction and temperature must be float or int\n")
            self.__propellant_v_condition = 0
            return
        #  assessing fuel coherence
        if fuel is not None:
            for i in fuel:
                if len(i) == 3:
                    if (type(i[0]) is str) and (type(i[1]) is int or float) and (type(i[2]) is int or float):
                        pass
                    elif (type(i[0]) is str) and (type(i[1]) is int or float) and (type(i[2]) is int or float):
                        pass
                    else:
                        log.error("CEA: Input propellant method\n"
                                  "FUEL - Oxid and fuel parameters must be a list inside a list, like:\n"
                                  "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one\n"
                                  "-instruction:\n"
                                  "name must be string, mass fraction and temperature must be float or int\n")
                        self.__propellant_v_condition = 0
                        return
                else:
                    log.error("CEA: Input propellant method\n"
                              "FUEL -  Oxid and fuel parameters must be a list inside a list, like:\n"
                              "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one\n"
                              "- instruction:\n"
                              "name must be string, mass fraction and temperature must be float or int\n")
                    self.__propellant_v_condition = 0
                    return
            #  verifying existence of species
            for i in fuel:
                result_search = self.__search_input_propellants(i[0])
                if result_search == 0:
                    return
            # setting fuel
            self.__fuels = fuel
        elif oxid is None:
            log.error("CEA: Input propellant method\n"
                      "FUEL - Both oxid and fuel parameters are empty or not a list\n"
                      "CEA: Oxid and fuel parameters must be a list inside a list, like:\n"
                      "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one"
                      "- instruction:\n"
                      "name must be string, mass fraction and temperature must be float or int\n")
            self.__propellant_v_condition = 0
            return
        self.__propellant_v_condition = 1

    # input parameters
    def __islist(self, lista):
        if type(lista) is list:
            return 1
        else:
            log.info("CEA: Analysis {}".format(self.__case))
            log.error("CEA: Parameter: {}\nParameter is not a list".format(lista))
            log.warning("CEA: The input parameters should be inside a list, like:\n"
                        "chamber_pressure=[p1,p2],of=[0.5,1,2]"
                        "- Instruction: if just one value -> chamber_pressure=[p1]\n")
            return 0

    def input_parameters(self, combustion_temp=3800, chamber_pressure=None, sub_aeat=None,
                         sup_aeat=None, pipe=None, of_ratio=None, chem_ratio=None,
                         phi_ratio=None, fbyw_ratio=None):
        # reset conditions
        self.__chamber_pressure_cond = 0  # 0 disable, 1 enable
        self.__sub_aeat_cond = 0  # 0 disable, 1 enable
        self.__sup_aeat_cond = 0  # 0 disable, 1 enable
        self.__pipe_cond = 0  # 0 disable, 1 enable
        self.__of_ratio_cond = 0  # 0 disable, 1 enable
        self.__chem_ratio_cond = 0
        self.__phi_ratio_cond = 0
        self.__fbyw_ratio_cond = 0
        # assessing mixture ratios
        if ((phi_ratio is None) and (chem_ratio is None)) and (of_ratio is None):
            log.error("CEA: Input parameters\n"
                      "phi_ratio and chem_ratio and of_ratio are empty")
            log.warning("CEA: case: {} - Parameters input methods\n"
                        "Instruction: A Least one of the three mixture\n"
                        "ratios must receive a value".format(self.__case))
            log.info("-Input parameters are empty\n")
            self.__input_parameters_condition = 0
            return
        # setting temperature
        self.__combustion_temp = combustion_temp
        # setting chamber pressure
        if chamber_pressure is None:
            log.error("CEA:  Input parameters\n"
                      "Chamber pressure need a least a value")
            log.warning("CEA: case: {} - Parameters input methods\n"
                        "Instruction: A Least one of the three mixture\n"
                        "ratios must receive a value\n".format(self.__case))
            self.__input_parameters_condition = 0
            return
        else:
            result = self.__islist(chamber_pressure)
            if result == 1:
                self.__chamber_pressure_cond = 1
                self.__chamber_pressure = chamber_pressure
            else:
                self.__input_parameters_condition = 0
                return
        # sub ae/at
        if sub_aeat is not None:
            result = self.__islist(sub_aeat)
            if result == 1:
                self.__sub_aeat_cond = 1
                self.__sub_aeat = sub_aeat
            else:
                self.__input_parameters_condition = 0
                return
        # sup ae/at
        if sup_aeat is not None:
            result = self.__islist(sup_aeat)
            if result == 1:
                self.__sup_aeat_cond = 1
                self.__sup_aeat = sup_aeat
            else:
                self.__input_parameters_condition = 0
                return
        # pipe
        if pipe is not None:
            result = self.__islist(pipe)
            if result == 1:
                self.__pipe_cond = 1
                self.__pipe = pipe
            else:
                self.__input_parameters_condition = 0
                return
        # of_ratio
        if of_ratio is not None:
            result = self.__islist(of_ratio)
            if result == 1:
                self.__of_ratio_cond = 1
                self.__of_ratio = of_ratio
            else:
                self.__input_parameters_condition = 0
                return
        # chem_ratio
        if chem_ratio is not None:
            result = self.__islist(chem_ratio)
            if result == 1:
                self.__chem_ratio_cond = 1
                self.__chem_ratio = chem_ratio
            else:
                self.__input_parameters_condition = 0
                return
        # phi_ratio
        if phi_ratio is not None:
            result = self.__islist(phi_ratio)
            if result == 1:
                self.__phi_ratio_cond = 1
                self.__phi_ratio = phi_ratio
            else:
                self.__input_parameters_condition = 0
                return
        # fbyw_ratio
        if fbyw_ratio is not None:
            result = self.__islist(fbyw_ratio)
            if result == 1:
                self.__fbyw_ratio_cond = 1
                self.__fbyw_ratio = fbyw_ratio
            else:
                self.__input_parameters_condition = 0
                return
        self.__input_parameters_condition = 1

    def output_parameters(self, user_outputs):
        if type(user_outputs) is str:
            if user_outputs == 'all':
                # thermodynamical properties
                self.__out_p = 1
                self.__out_t = 1
                self.__out_rho = 1
                self.__out_h = 1
                self.__out_u = 1
                self.__out_g = 1
                self.__out_s = 1
                self.__out_m = 1
                self.__out_mw = 1
                self.__out_cp = 1
                self.__out_gam = 1
                self.__out_son = 1
                # rocket performance
                self.__out_pipe = 1
                self.__out_mach = 1
                self.__out_aeat = 1
                self.__out_cf = 1
                self.__out_ivac = 1
                self.__out_isp = 1
                # transport properties
                self.__out_vis = 1
                self.__out_cond = 1
                self.__out_condfz = 1
                self.__out_pran = 1
                self.__out_pranfz = 1
                # fuel-oxidante mixtures
                self.__out_fbw_ratio = 1  # %f
                self.__out_chem_eq_ratio = 1  # r,eq.ratio
                self.__out_phi_eq_ratio = 1  # phi,eq.ratio
                self.__out_of_ratio = 1  # o/f
                # setting up simulation
                self.__output_parameters_condition = 1
                return
            else:
                self.__output_parameters_condition = 0
                log.error("CEA: - Output parameters method\n{} not available in outputs".format(user_outputs))
                log.warning("- Instruction: Outputs parameters must be 'all' or a list, like: ['isp','cf']\n"
                            "- Outputs available: {}\n".format(user_outputs, self.__output_list))

        elif type(user_outputs) is list:
            for i in user_outputs:
                if i.lower() in self.__output_list:
                    pass
                else:
                    self.__output_parameters_condition = 0
                    log.error("CEA: - Output parameters method\n {} not available in outputs".format(i))
                    log.warning("- Instruction: Outputs parameters must be 'all' or a list, like: ['isp','cf']\n"
                                "- Outputs available: {}\n".format(self.__output_list))
                    return
        else:
            log.error("CEA: - Output parameters method\n"
                      "Outputs parameters must be 'all' or a list, like: ['isp','cf']\n"
                      "- Outputs available: {}\n".format(self.__output_list))
            self.__output_parameters_condition = 0
            return
        user_outputs = [s.replace(s, s.lower()) for s in user_outputs]
        # thermodynamical properties
        if 'p' in user_outputs:
            self.__out_p = 1
        if 't' in user_outputs:
            self.__out_t = 1
        if 'rho' in user_outputs:
            self.__out_rho = 1
        if 'h' in user_outputs:
            self.__out_h = 1
        if 'u' in user_outputs:
            self.__out_u = 1
        if 'g' in user_outputs:
            self.__out_g = 1
        if 's' in user_outputs:
            self.__out_s = 1
        if 'm' in user_outputs:
            self.__out_m = 1
        if 'mw' in user_outputs:
            self.__out_mw = 1
        if 'cp' in user_outputs:
            self.__out_cp = 1
        if 'gam' in user_outputs:
            self.__out_gam = 1
        if 'son' in user_outputs:
            self.__out_son = 1
        # rocket performance
        if 'pipe' in user_outputs:
            self.__out_pipe = 1
        if 'mach' in user_outputs:
            self.__out_mach = 1
        if 'aeat' in user_outputs:
            self.__out_aeat = 1
        if 'cf' in user_outputs:
            self.__out_cf = 1
        if 'ivac' in user_outputs:
            self.__out_ivac = 1
        if 'isp' in user_outputs:
            self.__out_isp = 1
        # transport properties
        if 'vis' in user_outputs:
            self.__out_vis = 1
        if 'cond' in user_outputs:
            self.__out_cond = 1
        if 'condfz' in user_outputs:
            self.__out_condfz = 1
        if 'pran' in user_outputs:
            self.__out_pran = 1
        if 'pranfz' in user_outputs:
            self.__out_pranfz = 1
        # fuel-oxidant mixtures
        if '%f' in user_outputs:
            self.__out_fbw_ratio = 1  # %f
        if 'o/f' in user_outputs:
            self.__out_of_ratio = 1  # o/f
        if 'phi,eq.ratio' in user_outputs:
            self.__out_phi_eq_ratio = 1  # phi,eq.ratio
        if 'r,eq.ratio' in user_outputs:
            self.__out_chem_eq_ratio = 1  # r,eq.ratio
        self.__output_parameters_condition = 1

    def settings(self, frozen='yes', freezing_point='exit', equilibrium='yes', short='yes', transport='yes'):

        #  frozen condition
        frozen = str(frozen)
        if frozen.lower() == 'yes':
            self.__nfz_cond = 1
            if (freezing_point == 'combustor') or (freezing_point == 1):
                self.__nfz = 1
            if (freezing_point == 'throat') or (freezing_point == 2):
                self.__nfz = 2
            if (freezing_point == 'exit') or (freezing_point == 3):
                self.__nfz = 3
        elif frozen.lower() == 'no':
            self.__nfz_cond = 0
        else:
            log.error("CEA: Settings method\n"
                      "Wrong frozen parameter")
            log.warning("CEA: Frozen simulation parameter must be 'yes' or 'no'\n")
            self.__setting_parameters_condition = 0
            return

        #  equilibrium condition
        equilibrium = str(equilibrium)
        if equilibrium.lower() == 'yes':
            self.__equilibrium = 1
        elif equilibrium.lower() == 'no':
            self.__equilibrium = 0
        else:
            log.error("CEA: Settings method\n"
                      "Wrong equilibrium parameter")
            log.warning("CEA: Equilibrium simulation parameter must be 'yes' or 'no'\n")
            self.__setting_parameters_condition = 0
            return

        #  enable short output
        short = str(short).lower()
        if short == 'yes':
            self.__short = 1
        elif short == 'no':
            self.__short = 0
        else:
            log.error("CEA: Settings method\n"
                      "Wrong short parameter")
            log.warning("CEA: Short output simulation parameter must be 'yes' or 'no'\n")
            self.__setting_parameters_condition = 0
            return

        #  enable transport properties
        transport = str(transport).lower()
        if transport == 'yes':
            self.__transport = 1
        elif transport == 'no':
            self.__transport = 0
        else:
            log.error("CEA: Settings method\n"
                      "Wrong transport parameter")
            log.warning("CEA: Transport properties simulation parameter must be 'yes' or 'no'\n")
            self.__setting_parameters_condition = 0
            return
        self.__setting_parameters_condition = 1

    def show_inp_file(self, type_f='logical'):
        if type_f == 'logical':
            if len(type_f) == 0:
                log.info('CEA: Show input file method\n'
                         '{} logical input file is empty\n'.format(self.__case))
            else:
                print('CEA: Show input file method\n'
                      '{} LOGICAL INPUT FILE:\n'.format(self.__case))
                print(self.__input_text_string)
        elif type_f == 'file':
            # getting data.csv
            os.chdir(self.__caminho_raiz)
            if os.path.exists('cea-exec/{}.inp'.format(self.__case)):
                file_inp = open('cea-exec/{}'.format(self.__file_name), 'r')
                file_inp = file_inp.readlines()
                print('CEA: Show input file method\n'
                      '{} INPUT FILE IN THE CEA DIRECTORY:\n'.format(self.__case))
                for i in file_inp:
                    print(i)
            else:
                log.info('CEA: Show input file method\n'
                         '{} input file in the CEA directory do not exists\n'.format(self.__case))
        else:
            log.error("CEA: Show input file method\n"
                      "Wrong option parameter")
            log.warning("CEA: option must be 'logical' or 'file'\n"
                        "- logical: file in the program\n"
                        "- file: file in the directory of CEA\n")

    def create_input_text(self):
        # clearing variables
        self.__input_text = []
        self.__input_text_string = ''

        # ADDING SETTINGS
        # first line
        primeira_linha = 'problem case={}\n'.format(self.__case)
        # second line
        segunda_linha = '   rocket'
        if self.__equilibrium == 1:
            segunda_linha = segunda_linha + ' equilibrium'
        if self.__nfz_cond == 1:
            segunda_linha = segunda_linha + ' frozen nfz={}'.format(self.__nfz)
        if self.__combustion_temp != 3800:
            segunda_linha = segunda_linha + ' tcest,k={}'.format(self.__combustion_temp)
        segunda_linha = segunda_linha + '\n'
        self.__input_text.append(primeira_linha)
        self.__input_text.append(segunda_linha)

        # ADDING INPUTS
        # adding pressure
        pressure = ' p,bar='
        for i in self.__chamber_pressure:
            pressure = pressure + ('{},'.format(i))
        self.__input_text.append(pressure + '\n')
        # adding pipe
        if self.__pipe_cond == 1:
            pipe = ' pi/p='
            for i in self.__pipe:
                pipe = pipe + ('{},'.format(i))
            self.__input_text.append(pipe + '\n')

        # adding aeat subsonic
        if self.__sub_aeat_cond == 1:
            aeatsub = ' sub,ae/at='
            for i in self.__sub_aeat:
                aeatsub = aeatsub + ('{},'.format(i))
            # self.input_text.append(aeatsub + '\n')

        # adding aeat supersonic
        if self.__sup_aeat_cond == 1:
            aeatsup = ' sup,ae/at='
            for i in self.__sup_aeat:
                aeatsup = aeatsup + ('{},'.format(i))
            self.__input_text.append(aeatsup + '\n')
        # adding o/f
        if self.__of_ratio_cond == 1:
            of_ratio = ' o/f='
            for i in self.__of_ratio:
                of_ratio = of_ratio + ('{},'.format(i))
            self.__input_text.append(of_ratio + '\n')
        # adding chemical ratio
        if self.__chem_ratio_cond == 1:
            chem_ratio = 'r,eq.ratio='
            for i in self.__chem_ratio:
                chem_ratio = chem_ratio + ('{},'.format(i))
            self.__input_text.append(chem_ratio+'\n')
        # adding equivalence ratio - phi,eq.ratio
        if self.__phi_ratio_cond == 1:
            phi_ratio = 'phi,eq.ratio='
            for i in self.__phi_ratio:
                phi_ratio = phi_ratio + ('{},'.format(i))
            self.__input_text.append(phi_ratio+'\n')
        # adding percent fuel by weight ratio - %f
        if self.__fbyw_ratio_cond == 1:
            fbyw_ratio = '%f='
            for i in self.__fbyw_ratio:
                fbyw_ratio = fbyw_ratio + ('{},'.format(i))
            self.__input_text.append(fbyw_ratio+'\n')

        # ADDING PROPELLANTS
        # react
        self.__input_text.append('react\n')
        # adding fuels
        if self.__fuels is not None:
            for i in self.__fuels:
                self.__input_text.append(' fuel={} wt={} t,k={}\n'.format(i[0], i[1], i[2]))
        else:
            log.error("CEA: Creating input\n"
                      "- FUEL PARAMETER IS EMPTY\n"
                      "- Oxid must be a list inside a list, like:\n"
                      "[[name,mass fraction,temp],[same]] (more than one or [[same]] if just one")
        # adding oxidizers
        if self.__oxids is not None:
            for i in self.__oxids:
                self.__input_text.append(' oxid={} wt={} t,k={}\n'.format(i[0], i[1], i[2]))

        # ADDING OUTPUTS
        output = 'output siunits'
        if self.__short == 1:
            output = output + ' short'
        if self.__transport == 1:
            output = output + ' transpot'
        self.__input_text.append(output + '\n')
        # ADDING PLOTS
        plot = '    plot'
        # thermodynamical properties
        if self.__out_p == 1:
            plot += ' p'
        if self.__out_t == 1:
            plot += ' t'
        if self.__out_rho == 1:
            plot += ' rho'
        if self.__out_h == 1:
            plot += ' h'
        if self.__out_u == 1:
            plot += ' u'
        if self.__out_g == 1:
            plot += ' g'
        if self.__out_s == 1:
            plot += ' s'
        if self.__out_m == 1:
            plot += ' m'
        if self.__out_mw == 1:
            plot += ' mw'
        if self.__out_cp == 1:
            plot += ' cp'
        if self.__out_gam == 1:
            plot += ' gam'
        if self.__out_son == 1:
            plot += ' son'
        # rocket performance
        if self.__out_pipe == 1:
            plot += ' pip'
        if self.__out_mach == 1:
            plot += ' mach'
        if self.__out_aeat == 1:
            plot += ' aeat'
        if self.__out_cf == 1:
            plot += ' cf'
        if self.__out_ivac == 1:
            plot += ' ivac'
        if self.__out_isp == 1:
            plot += ' isp'
        # transport properties
        if self.__out_vis == 1:
            plot += ' vis'
        if self.__out_cond == 1:
            plot += ' cond'
        if self.__out_condfz == 1:
            plot += ' condfz'
        if self.__out_pran == 1:
            plot += ' pran'
        if self.__out_pranfz == 1:
            plot += ' pranfz'
        # mixture ratios
        if self.__out_fbw_ratio == 1:
            plot += ' %f'
        if self.__out_of_ratio == 1:
            plot += ' o/f'
        if self.__out_phi_eq_ratio == 1:
            plot += ' phi,eq.ratio'
        if self.__out_chem_eq_ratio == 1:
            plot += ' r,eq.ratio'
        # adding to the logical input file
        self.__input_text.append(plot + '\n')
        # adding end ot logical input file
        self.__input_text.append('end\n')

    def remove_analysis_file(self, name):
        os.chdir(self.__caminho_raiz)
        # .inp files
        if os.path.exists('cea-exec/{}.inp'.format(name)):
            os.remove('cea-exec/{}.inp'.format(name))
        # .out files
        if os.path.exists('cea-exec/{}.out'.format(name)):
            os.remove('cea-exec/{}.out'.format(name))
        # .plt files
        if os.path.exists('cea-exec/{}.plt'.format(name)):
            os.remove('cea-exec/{}.plt'.format(name))
        # .csv files
        if os.path.exists('cea-exec/{}.csv'.format(name)):
            os.remove('cea-exec/{}.csv'.format(name))

    def run(self):
        stt = self.__setting_parameters_condition
        ipc = self.__input_parameters_condition
        # output condition
        if self.__output_parameters_condition == 1:
            pass
        else:
            log.error("CEA: Run method\n"
                      "Output parameter not filled or configured properly")
            log.warning("CEA: Analysis not executed\n")
            self.remove_analysis_file(self.__case)
            return
        # propellant condition
        if self.__propellant_v_condition == 1:
            pass
        else:
            log.error("CEA: Run method\n"
                      "Propellant not filled or configured properly")
            log.warning("CEA: Analysis not executed\n")
            self.remove_analysis_file(self.__case)
            return
        if (stt == 1) and (ipc == 1):
            # creating input file
            self.create_input_text()
            # writing input file in the folder
            os.chdir(self.__caminho_raiz)
            with open('cea-exec/cea_python_input.txt', 'w') as inputbat:
                inputbat.write(self.__case)
            # excluindo arquivos anteriores
            self.remove_analysis_file(self.__case)
            # gravando no arquivo .inp
            arquivo = open('cea-exec/{}'.format(self.__file_name), 'w')
            for i in self.__input_text:
                self.__input_text_string = self.__input_text_string + str(i) + '\n'
            arquivo.write(self.__input_text_string)
            arquivo.close()
            # executando bat file
            os.chdir(self.__caminho_raiz + '/cea-exec/')
            os.startfile("cea_python.vbs")
            os.chdir(self.__caminho_raiz)
            sleep(1.5)
        elif stt == 0 and ipc == 1:
            log.error("CEA: Run method\n"
                      "Run Method - Settings not configured or \nnot filled right to perform CEA analysis")
            log.warning("CEA: Analysis not executed\n")
            self.remove_analysis_file(self.__case)
            return
        elif ipc == 0 and stt == 1:
            log.error("CEA: Run method\n"
                      "Run Method - Input parameters not configured\nor not filled right to perform CEA analysis")
            log.warning("CEA: Analysis not executed\n")
            self.remove_analysis_file(self.__case)
            return
        else:
            log.error("CEA: Run Method\n"
                      " - Settings and input parameters not configured\n"
                      "or not filled right to perform CEA analysis")
            log.warning("CEA: Analysis not executed\n")
            self.remove_analysis_file(self.__case)
            return

    def get_results(self, column_names='all', condition=3):
        # assessing file existence
        os.chdir(self.__caminho_raiz)
        if os.path.exists('cea-exec/{}.csv'.format(self.__case)):
            # assessing frozen condition
            if type(condition) is str:
                condition = str(condition).lower()
            elif type(condition) is int:
                pass
            else:
                log.error("CEA: Get results method\n"
                          "{} is not str or int".format(condition))
                log.warning("CEA: condition must be string or integer\n"
                            "- Options for condition: 'all', 'combustor' or '1', 'throat' or '2', 'exit' or '3'\n"
                            "CEA: columns must be string in the format of a list: \n"
                            "- Options for columns: 'all' or a list like:\n"
                            "['column name'] if one or ['name 1','name 2'] if more than one\n")
                return
            # assessing column names
            if type(column_names) is list:
                for i in column_names:
                    if type(i) is str:
                        pass
                    else:
                        log.error("CEA: Get results method\n"
                                  "{} item in {} is not a string".format(i, column_names))
                        log.warning("CEA: condition must be string or integer\n"
                                    "- Options for condition:\n"
                                    "'all', 'combustor' or '1', 'throat' or '2', 'exit' or '3'\n"
                                    "CEA: columns must be string in the format of a list: \n"
                                    "- Options for columns: 'all' or a list like:\n"
                                    "['column name'] if one or ['name 1','name 2'] if more than one\n")
                        return
                column_names = [s.replace(s, s.lower()) for s in column_names]
            elif type(column_names) is str:
                pass
            else:
                log.error("CEA: Get results method\n"
                          "{} parameter is not a string or list".format(column_names))
                log.warning("CEA: condition must be string or integer\n"
                            "- Options for condition: 'all', 'combustor' or '1', 'throat' or '2', 'exit' or '3'\n"
                            "CEA: columns must be string in the format of a list: \n"
                            "- Options for columns: 'all' or a list like:\n"
                            "['column name'] if one or ['name 1','name 2'] if more than one\n")
                return
            # getting data.csv
            df = pd.read_csv('cea-exec/{}.csv'.format(self.__case))
            # rename properly
            for i in df.columns:
                df.rename(columns={i: str(i).strip()}, inplace=True)
            # if all columns with all data are requested
            if (column_names == 'all') and (condition == 'all'):
                return df
            # if all columns with specific condition are requested
            elif (column_names == 'all') and (condition != 'all'):
                if (condition == 'combustor') or (condition == 1):
                    return self.__data_exit_condition(df, 0)
                elif (condition == 'throat') or (condition == 2):
                    return self.__data_exit_condition(df, 1)
                elif (condition == 'exit') or (condition == 3):
                    return self.__data_exit_condition(df, 2)
                elif type(condition) is int:
                    return self.__data_exit_condition(df, condition-1)
                else:
                    log.error("CEA: Get results method\n"
                              "Condition not informed properly")
                    log.warning("- Options to freezing point:\nall, exit, combustor, throat, 1, 2, 3, 4, 5\n")
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
                        log.error("CEA: Get results method\n"
                                  "{} is not in results".format(i))
                        log.info('- Column names available in results: {}\n'.format(df.columns))
                        return
                new_df = df[vectors_list_names]

                if (condition == 'combustor') or (condition == 1):
                    return self.__data_exit_condition(new_df, 0)
                elif (condition == 'throat') or (condition == 2):
                    return self.__data_exit_condition(new_df, 1)
                elif (condition == 'exit') or (condition == 3):
                    return self.__data_exit_condition(new_df, 2)
                elif condition == 'all':
                    return new_df
                elif type(condition) is int:
                    return self.__data_exit_condition(df, condition-1)
                else:
                    log.error("CEA: Get results method\n"
                              "Freezing point condition not informed properly")
                    log.warning("- Options: all, exit, combustor, throat or a integer\n"
                                "- For more information: McBride and Gordon (1994) and (1996)")
                    return
            else:
                log.error("CEA: Get results method\n"
                          "Column names are not informed properly")
                log.warning("- Options: all or list with specific names of columns\n"
                            "List of columns names available: \n"
                            "{}".format(df.columns))
                return
        else:
            log.error('CEA: Get Results Method\n'
                      '{} csv plot file in the CEA directory do not exists'.format(self.__case))
            log.info("CEA: Showing output file: \n")
            self.show_out_file()

    def __data_exit_condition(self, df, cond):
        df_new = self.__df_new
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

    def show_out_file(self):
        os.chdir(self.__caminho_raiz)
        if os.path.exists('cea-exec/{}.out'.format(self.__case)):
            print('CEA: {} OUTPUT FILE IN THE CEA DIRECTORY:\n'.format(self.__case))
            out_file = open('cea-exec/{}.out'.format(self.__case), 'r')
            out_file = out_file.readlines()
            for i in out_file:
                print(i)
        else:
            log.info("CEA: Show out file\n"
                     "{} output file in the CEA directory do not exists\n".format(self.__case))

    def get_simulation_file(self, type_file):
        os.chdir(self.__caminho_raiz)
        if type_file == 'out':
            if os.path.exists('cea-exec/{}.out'.format(self.__case)):
                out_file = open('cea-exec/{}.out'.format(self.__case), 'r')
                out_file = out_file.readlines()
                return out_file
            else:
                log.error('CEA: {} output file in the CEA directory do not exists\n'.format(self.__case))
        elif type_file == 'inp':
            if os.path.exists('cea-exec/{}'.format(self.__file_name)):
                file_inp = open('cea-exec/{}.inp'.format(self.__case), 'r')
                file_inp = file_inp.readlines()
                return file_inp
            else:
                log.error('CEA: {} input file in the CEA directory do not exists\n'.format(self.__case))
        else:
            log.error("CEA: get simulation file method\n"
                      "wrong type of file parameter")
            log.warning("CEA: type_file must be 'out' for output file or 'inp' for input file\n")
