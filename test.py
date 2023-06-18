from utils.speedzones import Preprocess, Speedzones
import pandas as pd
import numpy as np
import os
import openpyxl
from matplotlib import pyplot as plt
from utils.dataclass import pickled

###########
main_dir = 'C:\\Users\\User\\Downloads\\OneDrive_2023-05-22\\PhD Data'
all_data_dict = preprocess().all_data(main_dir)

pickled().pickling('C:\\Users\\User\\OneDrive\Desktop\\speed_zone_dict', all_data_dict)


data = pickled().open_jar('C:\\Users\\User\\OneDrive\Desktop\\speed_zone_dict')


test_frame = data['Team 1']['M1']['WD1A']
test_frame['a_magnitude'] = test_frame.apply(lambda x: (x[6]**2 + x[7]**2 + x[8]**2)**0.5, axis=1)
test_zone = Speedzones(test_frame)



def apply_zones(frame, zone_frame):



    return frame