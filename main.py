from entities import *
from utils import *
import json
import random
import numpy


boxdb = BoxDatabase()

def read_data(filename):
    f = open(filename, "r").read()
    f_json = json.loads(f)

    for item in f_json:
        size = item['size']
        mass = item['mass']
        fragile = item['fragile']
        is_rotatableXYZ = item['is_rotatableXYZ']

        boxdb.put(Box(size, mass, fragile, is_rotatableXYZ))




# box1 = Box([1, 2, 3], 5, True, [True, True, True])
# box1.position = [0, 0, 0]

boxdb.put(Box([1, 2, 3], 5, True, [True, True, True]))
boxdb.put(Box([1, 2, 3], 5, True, [True, True, True]))
boxdb.put(Box([4, 4, 2], 5, True, [True, True, True]))
boxdb.put(Box([2, 1, 2], 5, True, [True, True, True]))
boxdb.put(Box([7, 2, 3], 5, True, [True, True, True]))
boxdb.put(Box([7, 2, 2], 5, True, [True, True, True]))


boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)


cont = Container([10, 10, 10])

box1 = boxdb.get(1)




for i in boxdb.box_list:
    pos = find_place(cont, i)
    if pos != None:
        i.position = pos
        cont.put(i, i.position)
    print(i.position)






write_positions(boxdb, "PackerOUT/public/static/output.json")