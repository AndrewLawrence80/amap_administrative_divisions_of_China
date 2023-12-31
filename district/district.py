import numpy as np
from typing import List
from json import JSONEncoder


class District:
    """行政区划类型定义
    成员变量
    --------
        citycode: 城市编码
        adcode: 区域编码, 街道没有独有的adcode, 均继承父类(区县)的adcode
        name: 行政区名称
        center: 区域中心点
        level: 行政区划级别
    """

    def __init__(self, citycode: str, adcode: str, name: str, center: str, level: str, districts: List) -> None:
        self.citycode: str = citycode
        self.adcode: str = adcode
        self.name: str = name
        self.center: str = center
        self.level: str = level
        self.districts: List[District] = districts


class DistrictEncoder(JSONEncoder):
    def default(self, o: object):
        return o.__dict__
