from entities import *
from utils import *
import json
import random
import numpy as np
from drawing import draw
from settings import global_box_counter
import new_drawing

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




# boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
# boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)



boxdb.add(Box([2,1,1], 5, [True], [True]*3))
boxdb.add(Box([1,1,1], 5, [True], [True]*3))

block = Block([2,2,2], [True]*3)
block.put(boxdb.get(0), [0,0,0])
block.put(boxdb.get(1), [1,0,0])
boxdb.add(block)

#block.space_print()
cont = Container([4, 4, 4])
boxdb.get(0).rotateY()
cont.put(boxdb.get(0), [2, 1, 3])
cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)

new_drawing.draw("PackerOUT/public/static/output.json")
