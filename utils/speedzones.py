import numpy as np
import pandas as pd

class speedzone(object):

    def __init__(self, Dataframe):

        self.frame = Dataframe
        self.velocity = Dataframe[['velocity']]
        self.acceleration = Dataframe['acceleration']

    def random(self):

        return

class aggregate(object):