from utils.speedzones import speedzone
import pandas as pd
import numpy as np

v = [1, 2, 3, 4, 5]
a = [6, 7, 8, 9, 10]

frame = pd.DataFrame({'velocity': v, 'acceleration': a})


test = speedzone(frame) # works :)