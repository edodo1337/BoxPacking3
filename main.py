from entities import *
from utils import *
import json
import random
import numpy as np
from drawing import draw
from settings import global_box_counter
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
boxdb.add(Box([2,2,2], 5, [True], [True]*3))
boxdb.add(Box([2,2,2], 5, [True], [True]*3))

block = Block([6, 6, 4], [True] * 3)
block.put(boxdb.get(0), [0,0,0])
block.put(boxdb.get(1), [2,0,0])
block.put(boxdb.get(2), [0,0,2])

boxdb.add(block)
#block.space_print()

box = boxdb.get(0)
box.rotateZ()
print(box.diag)


# cont = Container([4, 4, 4])
#
# block.rotateZ()
# boxdb.get(0).rotateZ()
# cont.put(boxdb.get(0), [0,0,0])
# #cont.put(block, [0, 0, 0])
#
#
# #cont.pop(block)
#
# #cont.space_print()
# print('BOX COUNT', Box.get_count())
#
#
# write_positions(boxdb, "PackerOUT/public/static/output.json", cont)
#
# draw("PackerOUT/public/static/output.json")