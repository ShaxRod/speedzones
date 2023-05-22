from utils.speedzones import preprocess
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

read_pickle = pickled().open_jar('C:\\Users\\User\\OneDrive\\Desktop\\speed_zone_dict')