import requests
from district import District, DistrictEncoder
import json
import time
import os
from typing import List

URL = "https://restapi.amap.com/v3/config/district"
ROOT_PATH = "data"

web_key = None
with open("webapi_key.json", "r") as f:
    web_key = json.load(f)["key"]


def dfs(district: District, save_path: str):
    """递归处理三级行政区划"""
    # 如果当前已经处理到街道级，递归返回
    if district.level=="street":
        return
    # 保存当前地区
    save_path = os.path.join(save_path, district.name)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    with open(os.path.join(save_path,district.name)+".json", "w") as f:
        json.dump(district, f, ensure_ascii=False, indent=4, cls=DistrictEncoder)
    # 获取子地区地址递归执行
    district_list = []
    for district_dict in district.districts:
        district_list.append(District(district_dict["citycode"], district_dict["adcode"], district_dict["name"], district_dict["center"], district_dict["level"], district_dict["districts"]))
    for district in district_list:
        dfs(district, save_path)
    # 恢复因递归被扩展的路径
    save_path.rstrip(district.name)


def fetch_data():
    country = requests.get(URL, params={
        "keywords": "中华人民共和国",
        "subdistrict": 1,
        "key": web_key
    }).json()["districts"][0]

    with open(os.path.join(ROOT_PATH, "中华人民共和国") + ".json", "w") as f:
        json.dump(country, f, ensure_ascii=False, indent=4, cls=DistrictEncoder)

    province_name_list = []
    for province_dict in country["districts"]:
        province_name_list.append(province_dict["name"])

    for province_name in province_name_list:
        province_dict = requests.get(URL, params={
            "keywords": province_name,
            "subdistrict": 3,
            "key": web_key
        }).json()["districts"][0]
        province: District = District(province_dict["citycode"], province_dict["adcode"], province_dict["name"], province_dict["center"], province_dict["level"], province_dict["districts"])
        dfs(province, ROOT_PATH)
        # 控制每秒并发量
        time.sleep(0.05)


if __name__ == "__main__":
    fetch_data()
