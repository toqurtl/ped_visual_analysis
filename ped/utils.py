import numpy as np
import math
from pandas import DataFrame, Series

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def cart2pol_theta(x,y):
    rho, phi = cart2pol(x,y)
    return rho, phi / math.pi * 180

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def detected_time_range(data: DataFrame, time_str: str, column_str: str):    
    data = data[[time_str, column_str]]
    idx_list = []
    time_list = []
    for idx, row in data.iterrows():        
        if not np.isnan(row[column_str]):
            idx_list.append(idx)
            time_list.append(row[time_str])
        
    return {"time": np.array(time_list), "idx": np.array(idx_list)}

def not_nan_data(np_data):
    return np_data[np.logical_not(np.isnan(np_data))]
    
def to_interval(series: Series, interval):
    np_data = not_nan_data(series.to_numpy())
    new_list = []
    for idx, data in enumerate(np_data):
        if idx + interval < len(np_data):            
            new_list.append(np_data[idx:idx+interval].mean())
        else:
            new_list.append(np_data[idx:].mean())
    return np.array(new_list)

