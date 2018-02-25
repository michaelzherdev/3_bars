#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from math import cos, asin, sqrt

def load_data(filepath):
    data = ""
    with open(os.path.abspath(filepath), 'r') as f:
        data = f.read()
    return data


def get_biggest_bar(data):
    max_seats = max(get_bar_seats_num(data))
    features = json.loads(data)["features"]
    for i in range(0, len(features)):
        if(max_seats == features[i]["properties"]["Attributes"]["SeatsCount"]):
            return features[i]["properties"]["Attributes"]["Name"]


def get_smallest_bar(data):
    min_seats = min(get_bar_seats_num(data))
    features = json.loads(data)["features"]
    for i in range(0, len(features)):
       if(min_seats == features[i]["properties"]["Attributes"]["SeatsCount"]):
            return features[i]["properties"]["Attributes"]["Name"]

def get_bar_seats_num(data):
    res = []
    features = json.loads(data)["features"]
    for i in range(0, len(features)):
        res.append(features[i]["properties"]["Attributes"]["SeatsCount"])
    return res


def get_closest_bar(data, longitude, latitude):
    res = []
    features = json.loads(data)["features"]
    for i in range(0, len(features)):
        res.append(features[i]["geometry"]["coordinates"])
    clos_coord = min(res, key=lambda p: distance(longitude, latitude, p[0], p[1]))
    features = json.loads(data)["features"]
    for i in range(0, len(features)):
        if(clos_coord[0] == features[i]["geometry"]["coordinates"][0] and
                   clos_coord[1] == features[i]["geometry"]["coordinates"][1]):
            return features[i]["properties"]["Attributes"]["Name"]

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

if __name__ == '__main__':
    json_file_path = raw_input("Путь к json-файлу: ")
    data = load_data(json_file_path)
    big_bar = get_biggest_bar(data)
    small_bar = get_smallest_bar(data)

    lon = float(input("Введите широту: "))
    lat = float(input("Введите долготу: "))
    closest_bar = get_closest_bar(data, lon, lat)

    print("Самый большой бар: " + big_bar.encode('utf8'))
    print("Самый маленький бар: " + small_bar.encode('utf8'))
    print("Самый близкий бар: " + closest_bar.encode('utf8'))

