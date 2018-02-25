#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from math import cos, asin, sqrt


def load_data(filepath):
    with open(os.path.abspath(filepath), encoding="utf8") as f:
        text = f.read()
    return text


def get_biggest_bar(json_data):
    seats = max(_get_bar_seats_num(json_data))
    return _get_biggest_or_smallest_bar_name(json_data, seats=seats)


def get_smallest_bar(json_data):
    seats = min(_get_bar_seats_num(json_data))
    return _get_biggest_or_smallest_bar_name(json_data, seats=seats)


def _get_bar_seats_num(json_data):
    res = []
    features = json.loads(json_data)["features"]
    for feature in range(len(features)):
        res.append(features[feature]["properties"]["Attributes"]["SeatsCount"])
    return res


def _get_biggest_or_smallest_bar_name(json_data, seats):
    features = json.loads(json_data)["features"]
    for feature in range(len(features)):
        bar_attributes = features[feature]["properties"]["Attributes"]
        if (seats == bar_attributes["SeatsCount"]):
            return bar_attributes["Name"]


def get_closest_bar(json_data, lon, lat):
    res = []
    features = json.loads(json_data)["features"]
    for feature in range(len(features)):
        res.append(features[feature]["geometry"]["coordinates"])
    clos_coord = min(res, key=lambda crd: _distance(lon, lat, crd[0], crd[1]))
    features = json.loads(json_data)["features"]
    for feature in range(len(features)):
        bar_coords = features[feature]["geometry"]["coordinates"]
        if (clos_coord[0] == bar_coords[0] and clos_coord[1] == bar_coords[1]):
            return features[feature]["properties"]["Attributes"]["Name"]


def _distance(lat1, lon1, lat2, lon2):
    const = 0.017453292519943295
    arg_one = 0.5 - cos((lat2 - lat1) * const) / 2
    arg_two = cos(lat1 * const) * cos(lat2 * const)
    arg_three = (1 - cos((lon2 - lon1) * const)) / 2
    return 12742 * asin(sqrt(arg_one + arg_two * arg_three))


if __name__ == '__main__':
    json_file_path = input("Путь к json-файлу: ")
    json_data = load_data(json_file_path)
    big_bar = get_biggest_bar(json_data)
    small_bar = get_smallest_bar(json_data)

    lon = float(input("Введите широту: "))
    lat = float(input("Введите долготу: "))
    closest_bar = get_closest_bar(json_data, lon, lat)

    print("Самый большой бар: " + big_bar)
    print("Самый маленький бар: " + small_bar)
    print("Самый близкий бар: " + closest_bar)
