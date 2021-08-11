import numpy as np


class Time(object):
    def __init__(self, scene):
        self.time_array: np.array = None
        self.idx_array: np.array = None        

    def initialize(scene):
        pass

    def get_time(self, idx):
        if idx in self.idx_array:
            return self.time_array[idx]
        else:
            return None

    def get_idx(self, time):
        a = self.time_array[np.where(self.time_array==time)]
        if len(a) == 1:
            return a
        else:
            return None