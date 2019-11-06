from entities import *
from utils import *
import json
import random
import numpy as np


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


cont = Container([7, 7, 5])


boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([2, 2, 2], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))
boxdb.put(Box([1, 1, 1], 5, True, [True] * 3))






for i in boxdb.box_list:
    pos = find_place(cont, i)
    if pos!=None:
        cont.put(i, pos)

boxes = []
for i in range(2):
    #size = [random.choice(range(1,5))]*3
    size = [2,1,1]
    boxes.append(Box(size, 5, True, [True, True, True]))

boxes.append(Box([1, 1, 1], 5, True, [True, True, True]))


for i in boxes:
    boxdb.put(i)

block = Block([3, 3, 1], [True] * 3)
boxdb.put(block)
block.put(boxes[0], [0, 0, 0])
block.put(boxes[1], [0, 1, 0])
block.put(boxes[2], [2, 0, 0])




block.rotateX()

position = find_place(cont, block)
print(position)
cont.put(block, position)



#cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)