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
            match_dictionary[position] = pd.read_excel(directory, position)
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
                sheets = preprocess().get_sheets(game_dir)
                match_dict = preprocess().game_dict(sheets, game_dir)
                team_dict[game] = match_dict

            all_data[team] = team_dict
        return all_data


class Speedzones(object):

    def __init__(self, Dataframe):

        self.frame = Dataframe
        self.velocity = Dataframe[[' Speed']]
        self.acceleration = Dataframe[[' Accel X', ' Accel Y', ' Accel Z']]

    def velocity_zones(self, distribution_type: str = 'right-skew'):
        '''

        :param distribution_type: normal, right-skew
        :return: dictionary with velocity zones
        '''
        # function returns velocity zones for netball players. Left skewed distributions have been observed

        velocity = self.velocity
        speed_zones = dict()

        # bounds
        speed_zones['0'] = velocity.min()  # minimum velocity

        mu = velocity.mean()  # mean
        sigma = velocity.std()  # standard deviation

        if distribution_type == 'right-skew':
            for i in range(1, 6):
                speed_zones[i] = speed_zones['0'] + sigma * i
        elif distribution_type == 'normal':
            for i, j in enumerate(range(-2, 3)):
                speed_zones[i + 1] = mu + j * sigma

        speed_zones['6'] = velocity.max()  # maximum velocity

        return speed_zones

    def acceleration_zones(self, distribution_type: str = 'normal'):
        '''

        :param distribution_type: normal, right-skew
        :return: dictionary with velocity zones
        '''

        speed_zones = dict()
        acceleration = self.acceleration
        magnitude = (acceleration[' Accel X'] ** 2 +
                     acceleration[' Accel Y'] ** 2 +
                     acceleration[' Accel Z'] ** 2) ** 0.5


        # bounds
        speed_zones['0'] = magnitude.min()  # minimum velocity

        mu = magnitude.mean()  # mean
        sigma = magnitude.std()  # standard deviation

        if distribution_type == 'right-skew':
            for i in range(1, 6):
                speed_zones[i] = speed_zones['0'] + sigma * i
        elif distribution_type == 'normal':
            for i, j in enumerate(range(-2, 3)):
                speed_zones[i + 1] = mu + j * sigma

        speed_zones['6'] = magnitude.max()  # maximum velocity

        return speed_zones
