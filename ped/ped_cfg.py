import json
from enum import Enum


with open("ped\\default.json", "r") as f:
    cfg = json.load(f)


def offspring(key):
    return cfg["csv"]["offspring"][key]

def item_list():
    return cfg["csv"]["item_list"]

def v_mean_max():
    return cfg["analysis"]["outlier"]["v_mean"]["max"]


def v_mean_min():
    return cfg["analysis"]["outlier"]["v_mean"]["min"]


def d_mean_p_max():
    return cfg["analysis"]["outlier"]["d_mean_p"]["max"]


def d_mean_p_min():
    return cfg["analysis"]["outlier"]["d_mean_p"]["min"]


def d_mean_n_max():
    return cfg["analysis"]["outlier"]["d_mean_n"]["max"]


def d_mean_n_min():
    return cfg["analysis"]["outlier"]["d_mean_n"]["min"]


def time_unit_for_sec():
    return cfg["analysis"]["time_unit_for_sec"]

def exception_dict():
    return cfg["analysis"]["position"]["exception"]

def door_position():
    return cfg["analysis"]["position"]["exception"]["door"]["h"], cfg["analysis"]["position"]["exception"]["door"]["v"]

def door_2_position():
    return cfg["analysis"]["position"]["exception"]["door_2"]["h"], cfg["analysis"]["position"]["exception"]["door_2"]["v"]