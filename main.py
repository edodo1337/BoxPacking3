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
for i in range(3):
    #size = [random.choice(range(1,5))]*3
    size = [1,1,1]
    boxes.append(Box(size, 5, True, [True, True, True]))

boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)


cont = Container([3, 3, 3])

block = Block([2,2,2], [True]*3)

for ind, i in enumerate(boxes):
    block.put(i, [ind, 0, 0])

boxdb.put(block)

for i in boxdb.box_list:
    pos = find_place(cont, i)
    if pos != None:
        i.position = pos
        cont.put(i, i.position)



cont.space_print()

write_positions(boxdb, "PackerOUT/public/static/output.json", cont)