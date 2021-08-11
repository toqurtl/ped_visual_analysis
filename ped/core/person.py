from pandas.core.indexes.base import Index
from ped import utils
from ped.type import InfoType
from ped import ped_cfg as cfg
import numpy as np
from pandas import Series


def create_pos_info(person):
    np_h = person.measured_data(InfoType.HorizontalPosition).to_numpy()        
    np_v = person.measured_data(InfoType.VerticalPostion).to_numpy()
    np_h = np.expand_dims(np_h, axis=1)
    np_v = np.expand_dims(np_v, axis=1)
    person.pos = np.append(np_h, np_v, axis=1)
    person.start_pos = np.array([utils.not_nan_data(np_h)[0], utils.not_nan_data(np_v)[0]])
    person.finish_pos = np.array([utils.not_nan_data(np_h)[-1], utils.not_nan_data(np_v)[-1]])
    return


def create_exist_range(person):
    time_range = utils.detected_time_range(
                data=person.scene_data_map["hp"],
                time_str=person.scene.time_idx,
                column_str=person.person_idx
            )
    person.exist_time_range = time_range["time"]
    person.exist_idx_range = time_range["idx"]


def initialize(person):
    create_pos_info(person)
    create_exist_range(person)


class Person(object):
    def __init__(self, scene, person_idx):
        self.scene = scene        
        self.person_idx = person_idx
        
        # position info
        self.pos = None
        self.start_pos = None
        self.finish_pos = None

        # time range
        self.exist_time_range = None
        self.exist_idx_range = None

        # initialize
        initialize(self)
        return
        
    def measured_data(self, infotype: InfoType):
        return self.scene.measured_data(infotype)[self.person_idx]

    @property
    def scene_data_map(self):
        return self.scene.data_map

    @property
    def velocity_mean(self):
        return self.velocity_data.mean()

    @property
    def velocity_ratio(self):
        return self.velocity_data.to_numpy() / self.velocity_mean
    
    @property
    def direction_data(self):
        h_data = self.velocity_h_data
        v_data = self.velocity_v_data         
        r_data, di_data = utils.cart2pol_theta(h_data, v_data)        
        return di_data

    @property
    def direction_change_data(self):
        print(self.direction_data)
        print(self.velocity_h_data)
        return np.diff(self.direction_data) / self.scene.time_line.to_numpy()

    @property
    def direction_mean(self):
        return self.direction_data.mean()

    @property
    def direction_ratio(self):        
        return self.direction_data.to_numpy() / self.direction_mean

    @property
    def exist_time_interval(self):
        return (self.exist_time_range[-1] - self.exist_time_range[0]) / cfg.time_unit_for_sec()

    @property
    def velocity_avg(self):        
        return np.linalg.norm(self.finish_pos - self.start_pos, ord=2) / self.exist_time_interval   
    
    @property
    def direction_avg(self):   
        diff = self.finish_pos - self.start_pos
        _, theta = utils.cart2pol_theta(diff[0], diff[1])
        return theta

    @property
    def direction(self):
        return self.direction_avg > 0

    # time
    def time(self, idx):
        return self.scene.time(idx)

    def time_interval(self, start_idx, finish_idx):
        return self.scene.time_interval(start_idx, finish_idx)

    # interval(if interval=1 -> same as property)
    def velocity_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.velocity_data, interval)
        else:
            return utils.to_interval(self.velocity_data, interval)[idx]
        
    def velocity_v_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.velocity_v_data, interval)
        else:
            return utils.to_interval(self.velocity_v_data, interval)[idx]
        
    def velocity_h_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.velocity_h_data, interval)
        else:
            return utils.to_interval(self.velocity_h_data, interval)[idx]
        
    def acceleration_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.acceleration_data, interval)
        else:           
            return utils.to_interval(self.acceleration_data, interval)[idx]
        
    def acceleration_v_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.acceleration_v_data, interval)
        else:
            return utils.to_interval(self.acceleration_v_data, interval)[idx]
        
    def acceleration_h_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.acceleration_h_data, interval)
        else:
            return utils.to_interval(self.acceleration_h_data, interval)[idx]
        
    def position_v_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.position_v_data, interval)
        else:
            return utils.to_interval(self.position_v_data, interval)[idx]
        
    def position_h_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.position_h_data, interval)
        else:
            return utils.to_interval(self.position_h_data, interval)[idx]

    def direction_data_interval(self, interval, idx=-1):
        if idx==-1:
            return utils.to_interval(self.direction_data, interval)
        else:
            return utils.to_interval(self.direction_data, interval)[idx]

    # statistics
    def info_at_idx(self, idx, interval=1):
        return {            
            'person_id': self.scene.scene_id+"_"+self.person_idx,
            'scene_id': self.scene.scene_id,
            'group': self.scene.group_name,
            'num_person': self.scene.num_person,
            'a': self.acceleration_data_interval(interval=interval, idx=idx),            
            'v': self.velocity_data_interval(interval=interval, idx=idx),
            'hv': self.velocity_h_data_interval(interval=interval, idx=idx),
            'vv': self.velocity_v_data_interval(interval=interval, idx=idx),
            'hp': self.position_h_data_interval(interval=interval, idx=idx),
            'vp': self.position_v_data_interval(interval=interval, idx=idx),            
            'd': self.direction_data_interval(interval=interval, idx=idx),
            'v_ratio': self.velocity_data_interval(interval=interval, idx=idx) / self.velocity_mean,
            'd_ratio': self.direction_data_interval(interval=interval, idx=idx) / self.direction_mean
        }

    def to_dict(self):
        return {            
            'person_id': self.scene.scene_id+"_"+self.person_idx,
            'scene_id': self.scene.scene_id,
            'group': self.scene.group_name,
            'num_person': self.scene.num_person,
            'a_mean': self.acceleration_data.mean(),
            'a_std':  self.acceleration_data.std(),
            'v_mean': self.velocity_data.mean(),
            'v_std': self.velocity_data.std(),
            'd_mean': self.direction_data.mean(),
            'd_std': self.direction_data.std(),
            'v_mean_avg': self.velocity_avg,
            'd_mean_avg': self.direction_avg,
        }
    
    def to_dict_interval(self, interval):
        return {            
            'person_id': self.scene.scene_id+"_"+self.person_idx,
            'scene_id': self.scene.scene_id,
            'group': self.scene.group_name,
            'num_person': self.scene.num_person,
            'a_mean': self.acceleration_data_interval(interval).mean(),
            'a_std':  self.acceleration_data_interval(interval).std(),
            'v_mean': self.velocity_data_interval(interval).mean(),
            'v_std': self.velocity_data_interval(interval).std(),
            'd_mean': self.direction_data_interval(interval).mean(),
            'd_std': self.direction_data_interval(interval).std(),
            'v_mean_avg': self.velocity_avg,
            'd_mean_avg': self.direction_avg,
        }
        
    def to_pandas(self):        
        pass

    def is_exist(self, idx):
        return not np.isnan(self.position_at_idx(idx))

    def position_at_idx(self, idx):
        return self.pos[idx]

    def position(self):
        return self.pos
    
    def h_position_at_idx(self, idx):
        return self.pos[:,0][idx]

    def h_position(self):
        return self.pos[:,0]

    def v_position_at_idx(self, idx):
        return self.pos[:,1][idx]

    def v_position(self):
        return self.pos[:,1]

    # if nan -> at least one person doesn't exist
    def distance_at_idx(self, other, idx):
        return np.linalg.norm(self.pos[idx] - other.pos[idx], ord=2)

    def distance_with(self, other):
        print(self.pos-other.pos)
        exit()
        return np.linalg.norm(self.pos - other.pos, ord=2)

    def num_person_at_idx(self, idx, dis_min, dis_max):
        ctn = 0 
        for key, person in self.scene.person_dict.items():
            if self.person_idx != key:
                if person.is_exist(idx):
                    pass
