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
for i in range(6):
    #size = [random.choice(range(1,5))]*3
    size = [1,1,1]
    boxes.append(Box(size, 5, True, [True, True, True]))

for i in boxes:
    boxdb.put(i)

boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)


cont = Container([5, 5, 5])

block = Block([3,3,1], [True]*3)


for ind, i in enumerate(boxes[:3]):
    block.put(i, [ind, 0, 0])
for ind, i in enumerate(boxes[3:]):
    block.put(i, [0, ind, 0])



boxdb.put(block)

cont.put(block, [1, 0, 0])

box = Box([1,1,1], 5, True, [True]*3)
boxdb.put(box)

#block.rotateX()

cont.put(box, [1,0,1])


cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)