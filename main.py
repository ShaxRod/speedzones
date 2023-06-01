from utils.speedzones import Preprocess, Speedzones
import pandas as pd
import numpy as np
import os
import openpyxl
from matplotlib import pyplot as plt
from utils.dataclass import pickled

unprocessed_data__dir = 'C:\\Users\\User\\Downloads\\OneDrive_2023-05-22\\PhD Data'
output_dir = 'C:\\Users\\User\\OneDrive\\Desktop'
data_dict_dir = 'C:\\Users\\User\\OneDrive\\Desktop\\speed_zone_dict'

# labelled : position - university - a/b (two players) . csv
positions = ('GK', 'GS', 'GD', 'WA', 'WD', 'C', 'GA')

team = {'1': 'CPUT',
        '2': 'NMU',
        '3': 'WITS'}

# boolean paramaters
preprocess = False # preprocess data step : if already done set to False
H1 = True
H2 = False
H3 = False
H4 = False

def netball():

    if preprocess:
        data = preprocess().all_data(main_dir)
        pickled().pickling('C:\\Users\\User\\OneDrive\Desktop\\speed_zone_dict', all_data_dict)
        print("Data has been preprocessed and pickled")
    else:
        data = pickled().open_jar(data_dict_dir)
        print('Pickled data has been imported')


    # Hypothesis 1
    if H1:

        H1_frame_v = pd.DataFrame()
        H1_frame_a = pd.DataFrame()

        if os.path.exists(f'{output_dir}\\speedzone_outputs\\H1\\graphs') and os.path.exists(f'{output_dir}\\speedzone_outputs\\H1\\speedzones') :
            print('H1 directory exists')
        else:
            #os.mkdir(f'{output_dir}\\speedzone_outputs')
            os.mkdir(f'{output_dir}\\speedzone_outputs\\H1')
            os.mkdir(f'{output_dir}\\speedzone_outputs\\H1\\graphs')
            os.mkdir(f'{output_dir}\\speedzone_outputs\\H1\\speedzones')

        for team in data:
            for match in data[team]:
                for player in data[team][match]:

                    frame = data[team][match][player]
                    zone = Speedzones(frame)

                    velocity_frame = pd.DataFrame(zone.velocity_zones())
                    velocity_frame['player'] = player

                    acceleration_frame = pd.DataFrame([zone.acceleration_zones()])
                    acceleration_frame['player'] = player

                    H1_frame_v = pd.concat((H1_frame_v, velocity_frame), axis=0)
                    H1_frame_a = pd.concat((H1_frame_v, acceleration_frame), axis=0)


                    H1_frame_v.to_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\velocity.xlsx')
                    H1_frame_a.to_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\acceleration.xlsx')

# Hypotheis 2


# Hypotheis 3

# Hypothesis 4




if __name__ == '__main__':
    netball()

