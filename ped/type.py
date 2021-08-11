from enum import Enum
from ped.core.time import Time

class InfoType(Enum):
    HorizontalPosition = "hp"
    VerticalPostion = "vp"
    Velocity = "s"
    HorizontalVelocity = "hv"
    VerticalVelocity = "vv"
    Acceleration = "a"
    HorizontalAcceleration = "ha"
    VerticalAcceleration = "va"
    Direction = "d"
    DirectionChange = "dc"
    NewVelocity = "ns"
    NewHorizontalVelocity = "nhv"
    NewVerticalVelocity = "nvv"
    NewAcceleration = "na"
    NewHorizontalAcceleration = "ha"
    NewVerticalAcceleration = "va"
    
    def calculated_type():
        return [
            InfoType.Direction,
            InfoType.DirectionChange,
            InfoType.NewVelocity,
            InfoType.NewHorizontalVelocity,
            InfoType.NewVerticalVelocity,
            InfoType.NewAcceleration,
            InfoType.NewHorizontalAcceleration,
            InfoType.NewVerticalAcceleration
        ]

    def measured_type():
        return [
            InfoType.HorizontalPosition, 
            InfoType.VerticalPostion, 
            InfoType.Velocity,
            InfoType.HorizontalVelocity, 
            InfoType.VerticalVelocity, 
            InfoType.Acceleration,
            InfoType.HorizontalAcceleration, 
            InfoType.VerticalAcceleration
        ]
    
    def values():
        return [InfoType_type.value for InfoType_type in InfoType]

    def get_type(value):
        for InfoType_type in InfoType:
            if InfoType_type.value == value:
                return InfoType_type
        return

    def is_calculated_type(InfoType_type):        
        return InfoType_type in InfoType.calculated_type()

    def is_measured_type(InfoType_type):
        return InfoType_type in InfoType.measured_type()


class TimeType(Enum):
    Position = "position"
    Velocity = "velocity"
    Acceleration = "acceleration"

    def position_related_infotype():
        return [
            InfoType.HorizontalPosition,
            InfoType.VerticalPostion
        ]

    def velocity_related_infotype():
        return [
            InfoType.Velocity,
            InfoType.VerticalVelocity,
            InfoType.HorizontalVelocity
        ]

    def accerelation_related_infotype():
        return [
            InfoType.Acceleration,
            InfoType.HorizontalAcceleration,
            InfoType.VerticalAcceleration
        ]

    def related_infotype_map():
        return {
            TimeType.Position: TimeType.position_related_infotype(),
            TimeType.Velocity: TimeType.velocity_related_infotype(),
            TimeType.Acceleration: TimeType.accerelation_related_infotype(),
        }

    def get_time_type(infotype: InfoType):
        for timetype, related_list in TimeType.related_infotype_map().items():
            if infotype in related_list:
                return timetype
        return None                


class AnalysisType(Enum):
    MEAN = "mean"
    # .mean()
    DEVIATION = "std"
    # .std()
    AVG = "avg"

