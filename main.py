from utils.speedzones import Preprocess, Speedzones
import pandas as pd
import numpy as np
import os
import re
import openpyxl
from matplotlib import pyplot as plt
from utils.dataclass import pickled

# old_data =  'C:\\Users\\User\\Downloads\\OneDrive_2023-05-22\\PhD Data'
unprocessed_data__dir = r'C:\Users\User\Downloads\OneDrive_2023-06-15\Edited Raw data'

output_dir = 'C:\\Users\\User\\OneDrive\\Desktop'
data_dict_dir = 'C:\\Users\\User\\OneDrive\\Desktop\\speed_zone_dict'

# labelled : position - university - a/b (two players) . csv
position_group = ('GK', 'GS', 'GD', 'WA', 'WD', 'C', 'GA')

thirds_group = {'1': ('GS', 'GK'),
                '2': ('WA', 'WD', 'GA', 'GD'),
                '3': 'C'}

study_groups = {'defenders': ('GK', 'GD'),
                'mid-court': ('C', 'WA', 'WD'),
                'goalers': ('GS', 'GA')}

# boolean paramaters
preprocess = True # preprocess data step : if already done set to False
H1 = True
H2 = True
H3 = False
H4 = False

def netball():

    if preprocess:
        data = Preprocess().all_data(unprocessed_data__dir)
        pickled().pickling('C:\\Users\\User\\OneDrive\Desktop\\speed_zone_dict', data)
        print("Data has been preprocessed and pickled")
    else:
        data = pickled().open_jar(data_dict_dir)
        print('Pickled data has been imported')


    # Hypothesis 1
    # Speed zones per position (a,v) compare to gps system [Independent of time]
    # - positions (all teams merged)
    if H1:
        print('Running Hypothesis 1')
        # creating directories
        h1_directories = ['speedzone_outputs', 'H1', 'graphs', 'speedzones']
        dir_string = f'{output_dir}'

        for directory in h1_directories:
            dir_string_i = f'{dir_string}\\{directory}'
            if os.path.exists(dir_string_i):
                print(f'{dir_string_i} directory exists')
            else:
                os.mkdir(f'{dir_string_i}')
                print(f'{dir_string_i} directory created')

            dir_string = dir_string_i

        H1_frame_v = pd.DataFrame()
        H1_frame_a = pd.DataFrame()

        position_dict = dict()
        position_frame = pd.DataFrame()

        for group in position_group:
            for team in data:
                for match in data[team]:
                    for player in data[team][match]:

                        player_frame = data[team][match][player]
                        player_frame['player'] = player

                        if re.match(group, player):
                            position_frame = pd.concat((position_frame, player_frame), axis=0)
                        else:
                            print(f'{player} not a {group}')

            # exit aggregation loops
            position_dict[group] = position_frame   # store position aggregated frame to dictionary
            zone = Speedzones(position_frame)       # apply speed-zones to aggregated frames
            velocity_frame = pd.DataFrame(zone.velocity_zones())
            velocity_frame['position'] = group

            acceleration_frame = pd.DataFrame([zone.acceleration_zones()])
            acceleration_frame['position'] = group


            H1_frame_v = pd.concat((H1_frame_v, velocity_frame), axis=0)
            H1_frame_a = pd.concat((H1_frame_a, acceleration_frame), axis=0)

        pickled().pickling(f'{output_dir}\\speedzone_outputs\\H1\\aggregated_position_dict', position_dict)
        H1_frame_v.to_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\velocity.xlsx', index=False)
        H1_frame_a.to_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\acceleration.xlsx', index=False)


# Hypotheis 2

    if H2:
        print('Running Hypothesis 2')
        h2_directories = ['speedzone_outputs', 'H2', 'speedzones']
        dir_string = f'{output_dir}'

        for directory in h2_directories:
            dir_string_i = f'{dir_string}\\{directory}'
            if os.path.exists(dir_string_i):
                print(f'{dir_string_i} directory exists')
            else:
                os.mkdir(f'{dir_string_i}')

            dir_string = dir_string_i

            # importing speed-zone data
            if not H1:
                # velocity_zones = pd.read_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\velocity.xlsx')
                acceleration_zones = pd.read_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\acceleration.xlsx')
                position_dict = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H1\\aggregated_position_dict')
            else:
                # velocity_zones = H1_frame_v.copy()
                acceleration_zones = H1_frame_a.copy()


            # applying speed-zones
            for position in position_dict:

                position_agg_frame = position_dict[position].copy()
                position_agg_frame['Accel Magnitude 3D'] = (position_agg_frame['Accel X'] ** 2 +
                                                            position_agg_frame['Accel Y'] ** 2 +
                                                            position_agg_frame['Accel Z'] ** 2) ** 0.5

                position_acceleration_zones = acceleration_zones[acceleration_zones['position'] == position]

                # apply speed-zones
                position_dict[position]['acceleration zones'] = pd.cut(x=position_agg_frame['Accel Magnitude 3D'],
                                                     bins=position_acceleration_zones[['a0', 'a1', 'a2', 'a3',
                                                                                       'a4', 'a5']].values.tolist()[0],
                                                     labels=['zone 1', 'zone 2', 'zone 3', 'zone 4', 'zone 5'])

        pickled().pickling(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict', position_dict)









# Hypotheis 3

    if H3:

        h3_directories = ['speedzone_outputs', 'H3', 'speedzones']
        dir_string = f'{output_dir}'

        for directory in h2_directories:
            dir_string_i = f'{dir_string}\\{directory}'
            if os.path.exists(dir_string_i):
                print(f'{dir_string_i} directory exists')
            else:
                os.mkdir(f'{dir_string_i}')

            dir_string = dir_string_i

        if not H1:
            velocity_zones = pd.read_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\velocity.xlsx')
            acceleration_zones = pd.read_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\acceleration.xlsx')
        else:
            velocity_zones = H1_frame_v.copy()
            acceleration_zones = H1_frame_a.copy()


# Hypothesis 4




if __name__ == '__main__':
    netball()

