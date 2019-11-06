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



boxes = []
for i in range(2):
    #size = [random.choice(range(1,5))]*3
    size = [2,1,1]
    boxes.append(Box(size, 5, True, [True, True, True]))

for i in boxes:
    boxdb.put(i)

boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)


cont = Container([10, 10, 5])

block = Block([3,3,1], [True]*3)
block.put(boxes[0], [0,0,0])
block.put(boxes[1], [0,1,0])


# for ind, i in enumerate(boxes[:3]):
#     block.put(i, [ind, 0, 0])
# for ind, i in enumerate(boxes[3:]):
#     block.put(i, [0, ind, 0])



boxdb.put(block)



box1 = Box([1, 1, 1], 5, True, [True] * 3)
box2 = Box([1, 1, 1], 5, True, [True] * 3)
boxdb.put(box1, box2)

block.rotateY()

cont.put(block, [1, 0, 0])


cont.put(box1, [3, 1, 0])
cont.put(box2, [3, 0, 0])

#cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)