from ped.io import read_scene
from ped.core.person import Person
from ped import ped_cfg as cfg
from ped.type import InfoType, TimeType
from ped import utils
import numpy as np
from itertools import combinations


def set_data(scene):
    scene.data_path_map = read_scene.data_file_path_map(scene.folder_path)
    scene.data_map = read_scene.data_map(scene.folder_path)
    scene.person_idx_list = read_scene.person_index_list(scene.folder_path)
    scene.time_idx = read_scene.time_idx(scene.folder_path)
    return


def create_person(scene):
    for person_idx in scene.person_idx_list:
        p = Person(scene=scene, person_idx=person_idx)
        scene.person_dict[person_idx] = p
    return


def set_person_detected_time(scene):        
    for person_idx in scene.person_idx_list:
        detected_time = utils.detected_time_range(
            data=scene.data_map[InfoType.HorizontalPosition.value],
            time_str=scene.time_idx,
            column_str=person_idx

        )
        scene.person_detected_time[person_idx] = detected_time
    return


def calculate_data(scene):
    pass

def initialize(scene):
    set_data(scene)
    create_person(scene)
    set_person_detected_time(scene)
    return
    


class Scene(object):
    def __init__(self, folder_path, group_name="_"):
        # data origin information       
        self.folder_path = folder_path
        self.data_path_map = None

        # ID
        self.group_name = group_name   
        self.scene_id = group_name + "_scene_" + folder_path.split("\\")[-1]

        # person_info
        self.person_dict= {}        
        self.person_idx_list = None
        self.person_detected_time = {}
        
        # data
        self.data_map = None        
        self.time_idx = None
        
        # initialize
        initialize(self)
        return

    # get_data
    def measured_data(self, infotype: InfoType):
        return self.data_map[infotype.value]

    def get_time_idx(self, infotype: TimeType):
        return

    # utils
    @property
    def num_person(self):
        return len(self.person_dict)
    
    # time - index
    @property
    def time_line(self):
        return self.position_h_data[self.time_idx]

    @property
    def compare_person_list(self):
        return list(combinations(self.person_dict.values(), 2))

    def time(self, idx):
        return self.time_line[idx]

    def time_interval(self, start_idx, finish_idx):
        return (self.time(finish_idx) - self.time(start_idx)) / cfg.time_unit_for_sec()

    def person(self, person_idx):
        return self.person_dict[person_idx]

    # relationship between two people
    # def common_idx_list(self, p1: Person, p2: Person):        
    #     p1_range, p2_range = p1.exist_idx_range, p2.exist_idx_range
    #     return list(set(p1_range) & set(p2_range))

    def common_idx_list(self, p1_idx, p2_idx):
        p1, p2 = self.person_dict[p1_idx], self.person_dict[p2_idx]
        p1_range, p2_range = p1.exist_idx_range, p2.exist_idx_range
        return list(set(p1_range) & set(p2_range))

    def distance_of(self, p1_idx, p2_idx, idx: int):
        p1, p2 = self.person_dict[p1_idx], self.person_dict[p2_idx]
        p1_pos, p2_pos = p1.position_at_idx(idx), p2.position_at_idx(idx)        
        return np.linalg.norm(p1_pos-p2_pos, ord=2)

    def distance_list_of(self, p1_idx, p2_idx):
        distance_list = []
        for idx in self.common_idx_list(p1_idx, p2_idx):
            distance_list.append([idx, self.distance_of(p1_idx, p2_idx, idx)])
        return np.array(distance_list)

    def is_same_direction(self, p1_idx, p2_idx):
        p1, p2 = self.person_dict[p1_idx], self.person_dict[p2_idx]
        return p1.direction and p2.direction > 0

    def is_same_path(self, p1_idx, p2_idx, distance):
        p1, p2 = self.person_dict[p1_idx], self.person_dict[p2_idx]
        diff =  p1.position_h_data[p1.start_pos] - p2.position_h_data[p2.start_pos]
        return diff < distance

    def close_idx_list(self, p1_idx, p2_idx, distance):
        distance_list = self.distance_list_of(p1_idx, p2_idx)
        close_idx_list = []
        for d in distance_list:
            if d[1] < distance:
                close_idx_list.append(d[0])
        return close_idx_list

