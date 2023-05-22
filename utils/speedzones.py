import pandas as pd
import numpy as np
import os
import datetime
import openpyxl


class preprocess:
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

class speedzone(object):

    def __init__(self, Dataframe):

        self.frame = Dataframe
        self.velocity = Dataframe[['velocity']]
        self.acceleration = Dataframe['acceleration']

    def random(self):

        return
