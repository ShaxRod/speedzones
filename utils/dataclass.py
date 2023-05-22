import pandas as pd
import numpy as np
import os
import datetime
import pickle

class pickled:

    def pickling(self, name: str, data):
        """

        :param name: name of pickle file for storage
        :param dictionary: the input data type
        :return:
        """

        with open(f'{name}.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return pickle

    def open_jar(self, directory: str):

        with open(f'{directory}.pickle', 'rb') as handle:
            data_import = pickle.load(handle)

        return data_import