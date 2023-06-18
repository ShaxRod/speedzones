import pandas as pd
import numpy as np
import os
import datetime
import openpyxl


class Preprocess:
    ''' class to clean up data sets'''

    def get_sheets(self, directory: str):
        """

        :param directory: location of Excel workbook
        :return: the list of sheets in the Excel workbook
        """
        wb = openpyxl.load_workbook(directory)
        sheet_names = wb.sheetnames

        return sheet_names

    def game_dict(self, sheet_names: list, directory: str):

        """

        :param sheet_names: the list of sheets in the Excel workbook
        :param directory: location of Excel workbook
        :return: dictionary indexed by sheet entries which contains the sheets as data frames
        """

        match_dictionary = dict()
        for position in sheet_names:

            print(position)
            frame = pd.read_excel(directory, position)
            frame = frame.dropna(axis='columns')
            try:
                frame.columns = ['Match Phase', 'Real-Time Timestamp', 'Excel Timestamp', 'Speed',
                                 'Latitude', 'Longitude', 'Accel X', 'Accel Y', 'Accel Z']
                error = False
            except:
                print('error with data frame')
                error = True
            finally:
                frame['Time Delta'] = frame['Excel Timestamp'].diff(1)
                if error:
                    match_dictionary[position] = {'error': error, 'frame': frame}
                else:
                    match_dictionary[position] = frame

        return match_dictionary

    def all_data(self, main_dir: str):

        all_data = dict()
        teams = os.listdir(main_dir)

        for team in teams:
            print(team)
            team_dict = dict()
            team_dir = f'{main_dir}\\{team}'
            game_list = os.listdir(team_dir)

            for game in game_list:
                print(game)
                game_dir = f'{team_dir}\\{game}'
                sheets = Preprocess().get_sheets(game_dir)
                match_dict = Preprocess().game_dict(sheets, game_dir)
                team_dict[game[7:9]] = match_dict

            all_data[team] = team_dict
        return all_data


class Speedzones(object):

    def __init__(self, Dataframe):

        self.frame = Dataframe
        self.velocity = Dataframe[['Speed']]
        self.acceleration = Dataframe[['Accel X', 'Accel Y', 'Accel Z']]

    def velocity_zones(self, distribution_type: str = 'right-skew'):
        '''

        :param distribution_type: normal, right-skew
        :return: dictionary with velocity zones
        '''
        # function returns velocity zones for netball players. Left skewed distributions have been observed

        velocity = self.velocity
        speed_zones = dict()

        # bounds
        speed_zones['v0'] = velocity.min()  # minimum velocity

        mu = velocity.mean()  # mean
        sigma = velocity.std()  # standard deviation

        if distribution_type == 'right-skew':
            for i in range(1, 6):
                speed_zones['v' + str(i)] = speed_zones['v0'] + sigma * i
        elif distribution_type == 'normal':
            for i, j in enumerate([k for k in range(-2, 3) if k != 0]):
                speed_zones['v' + str(i + 1)] = mu + j * sigma

        speed_zones['v5'] = velocity.max()  # maximum velocity

        return speed_zones

    def acceleration_zones(self, distribution_type: str = 'normal', drop_z : bool = False):
        '''

        :param distribution_type: normal, right-skew
        :return: dictionary with velocity zones
        '''

        speed_zones = dict()
        acceleration = self.acceleration

        if drop_z:
            magnitude = (acceleration['Accel X'] ** 2 +
                         acceleration['Accel Y'] ** 2) ** 0.5
        else:
            magnitude = (acceleration['Accel X'] ** 2 +
                         acceleration['Accel Y'] ** 2 +
                         acceleration['Accel Z'] ** 2) ** 0.5

        # bounds
        speed_zones['a0'] = magnitude.min()  # minimum velocity

        mu = magnitude.mean()  # mean
        sigma = magnitude.std()  # standard deviation

        if distribution_type == 'right-skew':
            for i in range(1, 6):
                speed_zones['a' + str(i)] = speed_zones['a0'] + sigma * i
        elif distribution_type == 'normal':
            for i, j in enumerate([k for k in range(-2, 3) if k != 0]):
                speed_zones['a' + str(i + 1)] = mu + j * sigma

        speed_zones['a5'] = magnitude.max()  # maximum velocity

        return speed_zones

    def apply_zones(self, frame, aggregation):

        return frame
