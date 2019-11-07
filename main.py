from entities import *
from utils import *
import json
import random
import numpy as np
from drawing import draw


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


cont = Container([15, 15, 15])


boxdb.put(Box([4, 4, 4], 5, True, [True] * 3))
boxdb.put(Box([4, 4, 4], 5, True, [True] * 3))
boxdb.put(Box([4, 4, 4], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))
boxdb.put(Box([1, 2, 1], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))






# for i in boxdb.box_list:
#     pos = find_place(cont, i)
#     if pos!=None:
#         cont.put(i, pos)

boxes = []
for i in range(2):
    #size = [random.choice(range(1,5))]*3
    size = [6,2,2]
    boxes.append(Box(size, 5, True, [True, True, True]))

boxes.append(Box([1, 1, 1], 5, True, [True, True, True]))


for i in boxes:
    boxdb.put(i)

block = Block([6, 4, 2], [True] * 3)
boxdb.put(block)
block.put(boxes[0], [0, 0, 0])
block.put(boxes[1], [0, 2, 0])





#block.space_print()

block.rotateZ()



# position = find_place(cont, block)
# print(position)
cont.put(block, [0,0,0])



#cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)

draw("PackerOUT/public/static/output.json")