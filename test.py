from utils.speedzones import Preprocess, Speedzones
import pandas as pd
import numpy as np
import os
import openpyxl
from matplotlib import pyplot as plt
from utils.dataclass import pickled
import re

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

###########
aggregated_frames = pickled().open_jar(f'{output_dir}\\speedzone_outputs\\H2\\speed_zone_position_dict')
counts_dict = dict()
phase = ('First Half', 'Second Half')
for position in aggregated_frames:
    aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].str.strip()
    aggregated_frames[position]['Match Phase'] = aggregated_frames[position]['Match Phase'].apply( lambda x : phase[1] if re.match('Sec', x) else phase[0])

    for half in phase:

        counts = aggregated_frames[position][aggregated_frames[position]['Match Phase'] == half]['acceleration zones'].value_counts()
        counts_dict[f'{position}_{half}'] = counts
        counts.to_excel(f'{output_dir}\\speedzone_outputs\\H2\\speedzones\\H4_{position}_{half}_counts.xlsx')
