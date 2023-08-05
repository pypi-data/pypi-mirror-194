from enum import Enum


class MaskPositionPoint(str, Enum):
    FOREHEAD = "forehead"
    EYES = "eyes"
    MOUTH = "mouth"
    CHIN = "chin"
