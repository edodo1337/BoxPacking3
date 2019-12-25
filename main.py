from entities import *
from utils import *
import json
import random
import numpy as np
from drawing import draw
from settings import global_box_counter
import new_drawing
import random

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



cont = Container([CONT_X, CONT_Y, CONT_Z])


boxes = []

max_size = 5
for i in range(9):
    boxes.append(Box([random.randint(1, max_size) for i in range(3)], 5, [True], [True] * 3))
    #boxes.append(Box([2,2,3], 5, [True], [True] * 3))


#сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)



box_dict = { box.id:box for box in boxes }

for box in boxes:
    pos = find_place(cont, box, box_dict)
    if pos is not None:
        cont.put(box, pos)


write_positions("output.json", boxes)

# new_drawing.draw("PackerOUT/public/static/output.json")
new_drawing.draw("output.json", CONT_X, CONT_Y, CONT_Z)
