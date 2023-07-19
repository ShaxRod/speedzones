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
preprocess = False # preprocess data step : if already done set to False
H1 = False
H2 = False
H3 = False
H4 = False
H5 = False
H6 = True
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
        h1_directories = ['speedzone_outputs', 'H1', 'speedzones']
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
            position_frame = pd.DataFrame()
            for team in data:
                for match in data[team]:
                    for player in data[team][match]:

                        player_frame = data[team][match][player]
                        player_frame['player'] = player
                        player_frame['match'] = match

                        if re.match(group, player):
                            position_frame = pd.concat((position_frame, player_frame), axis=0)
                            print(f'{player}-{match} is a {group}')

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
                acceleration_zones = pd.read_excel(f'{output_dir}\\speedzone_outputs\\H1\\speedzones\\acceleration.xlsx')
                position_dict = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H1\\aggregated_position_dict')
            else:
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

        print('Hypothesis 2 completed')

# Hypotheis 3

    if H3:
        print('Running Hypothesis 3')
        h3_directories = ['speedzone_outputs',
                          'speedzone_outputs\\H3',
                          'speedzone_outputs\\H3\\counts',
                          'speedzone_outputs\\H3\\study groups',
                          'speedzone_outputs\\H3\\thirds']

        for directory in h3_directories:
            dir_string = f'{output_dir}\\{directory}'
            if os.path.exists(dir_string):
                print(f'{dir_string} directory exists')
            else:
                os.mkdir(f'{dir_string}')

        if not H2:
            aggregated_frames = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict')
        else:
            aggregated_frames = position_dict

        # position speed zone counts
        counts_dict = dict()

        for position in aggregated_frames:
            counts = aggregated_frames[position]['acceleration zones'].value_counts()
            counts_dict[position] = counts
            counts.to_excel(f'{output_dir}\\speedzone_outputs\\H3\\counts\\{position}_counts.xlsx')

        # study group counts
        for group in study_groups:
            group_frame = pd.DataFrame()

            for position in aggregated_frames:
                if position in study_groups[group]:
                    group_frame = pd.concat((group_frame, aggregated_frames[position]), axis=0)

            counts = group_frame['acceleration zones'].value_counts()
            counts.to_excel(f'{output_dir}\\speedzone_outputs\\H3\\study groups\\{group}_counts.xlsx')

        # thirds groups

        for third in thirds_group:
            third_frame = pd.DataFrame()

            for position in aggregated_frames:
                if position in thirds_group[third]:
                    third_frame = pd.concat((third_frame, aggregated_frames[position]), axis=0)

            counts = third_frame['acceleration zones'].value_counts()
            counts.to_excel(f'{output_dir}\\speedzone_outputs\\H3\\thirds\\{third}_counts.xlsx')

        print('Hypothesis 3 completed')
# Hypothesis 4

    if H4:
        print('Running Hypothesis 4')
        h4_directories = ['speedzone_outputs',
                          'speedzone_outputs\\H4',
                          'speedzone_outputs\\H4\\counts',
                          'speedzone_outputs\\H4\\study groups',
                          'speedzone_outputs\\H4\\thirds']

        for directory in h4_directories:
            dir_string = f'{output_dir}\\{directory}'
            if os.path.exists(dir_string):
                print(f'{dir_string} directory exists')
            else:
                os.mkdir(f'{dir_string}')
                print(f'{dir_string} directory exists has been created')

        if not H2:
            aggregated_frames = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict')
        else:
            aggregated_frames = position_dict

        # position speed zone counts
        counts_dict = dict()
        phase = ('First Half', 'Second Half')

        for position in aggregated_frames:
            aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].str.strip()
            aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].apply(
                lambda x: phase[1] if re.match('Sec', x) else phase[0])

            for half in phase:
                counts = aggregated_frames[position][aggregated_frames[position]['Match Phase'] == half]['acceleration zones'].value_counts()
                counts_dict[f'{position}_{half}'] = counts
                counts.to_excel(f'{output_dir}\\speedzone_outputs\\H4\\counts\\{position}_{half}_counts.xlsx')

        #study groups
        for group in study_groups:
            group_frame = pd.DataFrame()

            for position in aggregated_frames:
                aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].str.strip()
                aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].apply(
                    lambda x: phase[1] if re.match('Sec', x) else phase[0])
                if position in study_groups[group]:
                    group_frame = pd.concat((group_frame, aggregated_frames[position]), axis=0)

            for half in phase:
                counts = group_frame[group_frame['Match Phase'] == half]['acceleration zones'].value_counts()
                counts.to_excel(f'{output_dir}\\speedzone_outputs\\H4\\study groups\\{group}_{half}_counts.xlsx')



        # thirds groups
        for third in thirds_group:
            third_frame = pd.DataFrame()

            for position in aggregated_frames:
                if position in thirds_group[third]:
                    third_frame = pd.concat((third_frame, aggregated_frames[position]), axis=0)

            for half in phase:
                counts = third_frame['acceleration zones'].value_counts()
                counts.to_excel(f'{output_dir}\\speedzone_outputs\\H4\\thirds\\{third}_{half}_counts.xlsx')



        print('Hypothesis 4 completed')


    if H5:
        print('Running Hypothesis 5')

        h5_directories = ['speedzone_outputs',
                          'speedzone_outputs\\H5']

        for directory in h5_directories:
            dir_string = f'{output_dir}\\{directory}'
            if os.path.exists(dir_string):
                print(f'{dir_string} directory exists')
            else:
                os.mkdir(f'{dir_string}')
                print(f'{dir_string} directory exists has been created')

        if not H2:
            aggregated_frames = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict')
        else:
            aggregated_frames = position_dict

        player_dict = dict()
        iterator_c = 0
        phase = ('First Half', 'Second Half')
        for position in aggregated_frames:
            players = list(set(aggregated_frames[position]['player']))
            for player in players:
                player_frame = aggregated_frames[position][aggregated_frames[position]['player'] == player]

                #fixes
                '''player_frame['magnitude'] = (player_frame['Accel X'] ** 2 +
                                             player_frame['Accel Y'] ** 2 +
                                             player_frame['Accel Z'] ** 2) ** 0.5'''

                player_frame['Match Phase'] = player_frame['Match Phase'].str.strip()
                player_frame['Match Phase'] = player_frame['Match Phase'].apply(lambda x: phase[1] if re.match('Sec', x) else phase[0])


                temp = {'player': player,
                        'total acceleration counts': len(player_frame)
                        }

                # counter per zone
                counts = player_frame['acceleration zones'].value_counts()
                for i, j in enumerate(counts):
                    temp[f'{counts.index.to_list()[i]} totals counts'] = j
                #time spent
                for i, j in enumerate(counts):
                    temp[f'{counts.index.to_list()[i]} time in ms'] = j * 0.1

                # counts per half
                for half in phase:
                    phase_counts = player_frame[player_frame['Match Phase'] == half]['acceleration zones'].value_counts()
                    for i, j in enumerate(phase_counts):
                        temp[f'{phase_counts.index.to_list()[i]} {half} counts'] = j * 0.1

                player_dict[iterator_c] = temp
                iterator_c+=1

        frame = pd.DataFrame(player_dict)
        frame = frame.swapaxes('index', 'columns')
        frame.to_excel(f'{output_dir}\\speedzone_outputs\\H5\\player_frame.xlsx')

        print('Hypothesis 5 completed')

    if H6:
        print('Running Hypothesis 6')

        h6_directories = ['speedzone_outputs',
                          'speedzone_outputs\\H6']

        for directory in h6_directories:
            dir_string = f'{output_dir}\\{directory}'
            if os.path.exists(dir_string):
                print(f'{dir_string} directory exists')
            else:
                os.mkdir(f'{dir_string}')
                print(f'{dir_string} directory exists has been created')

        if not H2:
            aggregated_frames = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict')
        else:
            aggregated_frames = position_dict

        player_dict = dict()
        iterator_c = 0
        phase = ('First Half', 'Second Half')
        for position in aggregated_frames:
            players = list(set(aggregated_frames[position]['player']))
            for player in players:
                player_frame = aggregated_frames[position][aggregated_frames[position]['player'] == player]
                match_list = list(set(player_frame['match']))
                for match in match_list:
                    match_player_frame = player_frame[player_frame['match'] == match]
                    match_player_frame['Match Phase'] = match_player_frame['Match Phase'].str.strip()
                    match_player_frame['Match Phase'] = match_player_frame['Match Phase'].apply(
                        lambda x: phase[1] if re.match('Sec', x) else phase[0])
                    for half in phase:
                        phase_match_player = match_player_frame[match_player_frame['Match Phase'] == half]
                        #fixes
                        '''player_frame['magnitude'] = (player_frame['Accel X'] ** 2 +
                                                     player_frame['Accel Y'] ** 2 +
                                                     player_frame['Accel Z'] ** 2) ** 0.5'''




                        temp = {'player': player,
                                'match' : match,
                                'phase' : half,
                                'total acceleration counts': len(phase_match_player)
                                }

                        # counter per zone
                        counts = phase_match_player['acceleration zones'].value_counts()
                        for i, j in enumerate(counts):
                            temp[f'{counts.index.to_list()[i]} totals counts'] = j
                        #time spent
                        for i, j in enumerate(counts):
                            temp[f'{counts.index.to_list()[i]} time in ms'] = j * 0.1

                        # counts per half

                        player_dict[iterator_c] = temp
                        iterator_c+=1

        frame = pd.DataFrame(player_dict)
        frame = frame.swapaxes('index', 'columns')
        frame.to_excel(f'{output_dir}\\speedzone_outputs\\H6\\phase_match_player_frame.xlsx')

        print('Hypothesis 6 completed')


if __name__ == '__main__':
    netball()

