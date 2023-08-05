import csv
import re
import pandas as pd
import os
from typing import List, Dict

from steam_sdk.data.DataParsimConductor import DataParsimConductor, Coil
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing
from steam_sdk.utils.sgetattr import rsetattr, rgetattr
from steam_sdk.data.DataParsimConductor import Conductor


class ParsimConductor:
    """

    """

    def __init__(self, verbose: bool = True):
        """
        If verbose is read to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose

        # DataParsimConductor object that will hold all the information from the input csv file
        self.data_parsim_conductor = DataParsimConductor()
        self.column_name_magnets: str = ''
        self.column_name_coils: str = ''

    def read_from_input(self, path_input_file: str, groups_to_coils: Dict[str, List[int]], magnet_name: str):
        '''
        Read a .csv file and assign its content to a instance of DataParsimConductor().

        Parameters:
            path_input_file: Path to the .csv file to read
            groups_to_coils: dict that specifies which groups belong to which coils
        '''

        # read table into pandas dataframe
        if path_input_file.endswith('.csv'):
            df_conductors = pd.read_csv(path_input_file)
        elif path_input_file.endswith('.xlsx'):
            df_conductors = pd.read_excel(path_input_file)
        else:
            raise Exception(f'The extension of the file {path_input_file} is not supported.')
        df_conductors = df_conductors.dropna(axis=1, how='all')

        # Assign the content to a dataclass structure
        parsed_columns = []  # list containing the column names that were parsed
        for _, row in df_conductors.iterrows():
            self.__read_general_parameters(magnet_name)
            self.__read_magnet(row, parsed_columns)
            self.__read_coils(row, parsed_columns)
            self.__read_conductors(row, parsed_columns)

        # print out all the names of the ignored columns
        ignored_column_names = list(set(df_conductors.columns) - set(parsed_columns))
        if self.verbose: print(f'Names of ignored columns: {ignored_column_names}')

    def write_conductor_parameter_file(self, path_output_file: str, simulation_name: str, simulation_number: int):
        """
        Write the Parsim Conductor information to a CSV file, that can be used to run a ParsimSweep Step.

        Parameters:
            path_output_file (str): path to the output file
        """

        # Make target folder if it is missing
        make_folder_if_not_existing(os.path.dirname(path_output_file))

        # save all conductor parameters to chance in a dict
        dict_sweeper = dict()
        dict_sweeper['simulation_name'] = simulation_name
        dict_sweeper['simulation_number'] = int(simulation_number)
        self.__write_parsweep_general_parameters(dict_sweeper)
        self.__write_parsweep_magnet(dict_sweeper)
        self.__write_parsweep_coils(dict_sweeper)
        self.__write_parsweep_conductors(dict_sweeper)

        # open file in writing mode and write the dict of the parameters als a row in the csv file
        with open(path_output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=dict_sweeper.keys())
            writer.writeheader()
            writer.writerow(dict_sweeper)

    ################ HELPERS

    def __read_general_parameters(self, magnet_name):
        rsetattr(self.data_parsim_conductor, 'GeneralParameters.magnet_name', magnet_name)
        pass

    def __read_magnet(self, row, parsed_columns):

        # allowed names for the magnet
        csv_column_names_for_magnet_name = ['Magnet', 'Magnet Name']
        csv_column_names_for_coil_name = ['Coil', 'Coil Name']

        # find out what name is being used for the magnet and coil column and save it class wide (if not specified)
        if self.column_name_coils == '' or self.column_name_magnets == '':
            for magnet_name in csv_column_names_for_magnet_name:
                if magnet_name in row:
                    self.column_name_magnets = magnet_name
            for coil_name in csv_column_names_for_coil_name:
                if coil_name in row:
                    self.column_name_coils = coil_name

        # check if magnet name and coil name can be found
        if self.column_name_coils == '' or self.column_name_magnets == '':
            raise Exception(f'No column for magnet names or coil names could be found in the input table. Make sure these columns are present.\nallowed values for magnet name column:{csv_column_names_for_magnet_name}\nallowed values for coil name column:{csv_column_names_for_coil_name}')

        # if row belongs to the specified magnet
        if row[self.column_name_magnets] == self.data_parsim_conductor.GeneralParameters.magnet_name:
            # add coil name to Coils list
            self.data_parsim_conductor.Magnet.coils.append(row[self.column_name_coils])
            # and mark columns as parsed
            if self.column_name_magnets not in parsed_columns: parsed_columns.append(self.column_name_magnets)
            if self.column_name_coils not in parsed_columns: parsed_columns.append(self.column_name_coils)

    def __read_coils(self, row, parsed_columns):
        # if row belongs to the specified magnet
        if row[self.column_name_magnets] == self.data_parsim_conductor.GeneralParameters.magnet_name:

            # create Coil instance
            coil_name = row[self.column_name_coils]
            new_Coil = Coil()

            # check if coil name is valid
            if coil_name not in self.data_parsim_conductor.Magnet.coils:
                raise Exception('Unexpected error in steam_sdk.parsims.ParsimConductor.__read_coils(). Coil name previously not found.')
            if coil_name in self.data_parsim_conductor.Coils.keys():
                raise Exception(f'Coil names of the magnet {self.data_parsim_conductor.GeneralParameters.magnet_name} in column {self.column_name_coils} have to be unique. Name {coil_name} has been used before.')

            # change parameters of conductors instance
            dict_params = {
                'Coil ID': 'ID', 'ID': 'ID',
                'Cable ID': 'cable_ID', 'cable_ID': 'cable_ID',
                'Coil length': 'coil_length', 'coil_length': 'coil_length',
                'Coil RRR': 'coil_RRR', 'coil_RRR': 'coil_RRR',
                'Tref RRR low': 'T_ref_RRR_low', 'T_ref_RRR_low': 'T_ref_RRR_low',
                'Tref RRR high': 'T_ref_RRR_high', 'T_ref_RRR_high': 'T_ref_RRR_high',
                'Coil resistance room T': 'coil_resistance_room_T', 'coil_resistance_room_T': 'coil_resistance_room_T',
                'Tref coil resistance': 'T_ref_coil_resistance', 'T_ref_coil_resistance': 'T_ref_coil_resistance',
            }
            for csv_col_name, coil_param_name in dict_params.items():
                if csv_col_name in row:
                    # change parameter of Coil instance
                    if not pd.isna(row[csv_col_name]):
                        rsetattr(new_Coil, coil_param_name, row[csv_col_name])
                    # mark column as parsed
                    if csv_col_name not in parsed_columns: parsed_columns.append(csv_col_name)

            # set Conductor of the Coil and set weightfactor to 1.0
            new_Coil.conductors.append(f'conductor_{coil_name}')
            new_Coil.weight_conductors = [1.0]

            # append new coil instance to Coil Dict of ParsimConductor
            self.data_parsim_conductor.Coils.update({coil_name: new_Coil})

    def __read_conductors(self, row, parsed_columns):
        '''
        Function to read Conductors of ParsimConductors

        :param row: Series of parameters (read from csv file)
        :param parsed_columns: list of parsed table columns names
        '''
        # Ic_1: null ----> you won't find a corresponding parameter
        # T_ref_Ic_1: null ----> you won't find a corresponding parameter
        # B_ref_Ic_1: null ----> you won't find a corresponding parameter
        # Cu_noCu_sample_1: null ----> you won't find a corresponding parameter
        # Ic_2: null ----> you won't find a corresponding parameter
        # T_ref_Ic_2: null ----> you won't find a corresponding parameter
        # B_ref_Ic_2: null ----> you won't find a corresponding parameter
        # Cu_noCu_sample_2: null ----> you won't find a corresponding parameter
        # Cu_noCu_sample_2: null ----> you won't find a corresponding parameter

        # if row belongs to the specified magnet
        if row[self.column_name_magnets] == self.data_parsim_conductor.GeneralParameters.magnet_name:

            # create Conductor instance
            cond_name = f'conductor_{row[self.column_name_coils]}'
            new_Conductor = Conductor()

            # check if Conductor name is is valid (new conductor name corresponds to a conductor name already specified in a Coil)
            if cond_name not in sum([coil.conductors for coil in self.data_parsim_conductor.Coils.values()], []):
                raise Exception('Unexpected error in steam_sdk.parsims.ParsimConductor.__read_conductors(). Conductor name previously not found.')

            # change parameters of conductors instance
            dict_params = {
                'Ds [m]': 'strand_diameter', 'strand_diameter': 'strand_diameter',
                'Shape': 'shape', 'shape': 'shape',
                'Number of strands': 'number_of_strands', 'number_of_strands': 'number_of_strands',
                'width [m]': 'width', 'width': 'width',
                'Height [m]': 'height', 'height': 'height',
                'Cu noCu': 'Cu_noCu', 'Cu_noCu': 'Cu_noCu',
                'RRR [Ohm]': 'RRR',
                'Strand twist pitch': 'strand_twist_pitch', 'strand_twist_pitch': 'strand_twist_pitch',
                'Filament twist pitch': 'filament_twist_pitch', 'filament_twist_pitch': 'filament_twist_pitch',
                'F rho eff': 'f_rho_eff', 'f_rho_eff': 'f_rho_eff',
                'Ra [Ohm]': 'Ra',
                'Rc [Ohm]': 'Rc'
            }
            for csv_col_name, conductor_name in dict_params.items():
                if csv_col_name in row:
                    # change parameter
                    if not pd.isna(row[csv_col_name]):
                        rsetattr(new_Conductor, conductor_name, row[csv_col_name])
                    # mark column as parsed
                    if csv_col_name not in parsed_columns: parsed_columns.append(csv_col_name)

            # append new conductor instance to Conductors dictionary of ParsimConductor
            self.data_parsim_conductor.Conductors.update({cond_name: new_Conductor})

    def __write_parsweep_general_parameters(self, dict_sweeper):
        pass

    def __write_parsweep_magnet(self, dict_sweeper):
        # TODO conversion of the conductor groups
        # TODO Jc fit parameters from Ic measurements
        # TODO calculate average f_Cu
        # TODO calculate average RRR
        # TODO calculate coil length based on RT resistance
        pass

    def __write_parsweep_coils(self, dict_sweeper):
        pass

    def __write_parsweep_conductors(self, dict_sweeper):
        """
        Writes the Conductor parameter for a sweeper csv file to a dict.

        Parameters:
        - dict_sweeper (dict): input dict where the sweeper entries will be stored  int the format {columnName: value}

        """
        # parameter dict for creating the column names of sweeper csv file
        dict_param = {
            # format {parameter_name_of_conductor_object: parameter_name_of_DataModelMagnet_object} ~ TODO: check
            'strand_diameter': 'strand.diameter'
        }

        # looping through the conductor list
        for idx, (conductor_name, conductor) in enumerate(self.data_parsim_conductor.Conductors.items()):
            # get the number of the conductor from his name
            sweeper_cond_name = f'Conductors[{idx}].' #TODO: this assumes that the conductor list in model_data has the same order as the conductors in the csv file

            # parse data from DataParsimConductor to strings for sweeper csv and store them in dict_sweeper
            for cond_object_name, sweeper_name in dict_param.items():
                if rgetattr(conductor, cond_object_name):
                    dict_sweeper[sweeper_cond_name + sweeper_name] = rgetattr(conductor, cond_object_name)
