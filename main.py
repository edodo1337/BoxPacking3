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



boxdb.add(Box([4,2,2], 5, [True], [True]*3))

box = boxdb.get(0)
box.rotateX()
print(box.diag)

cont = Container([4, 4, 4])
cont.put(box, [0, 0, 0])

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)

new_drawing.draw("PackerOUT/public/static/output.json")
