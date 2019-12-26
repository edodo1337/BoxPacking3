from entities import *
from utils import *
import json
import new_drawing
import random

#boxdb = BoxDatabase()

cont = Container([CONT_X, CONT_Y, CONT_Z])
boxes = []



def read_data(filename):
#       чтение данных из файла
    f = open(filename, "r").read()
    f_json = json.loads(f)
    for item in f_json:
        print(item)
        if item['type'] == 'box':
            size = item['size']
            mass = item['mass']
            fragile = item['fragile']
            is_rotatableXYZ = item['is_rotatableXYZ']
            count = item['count']
            #boxes.extend([Box(size=size, mass=mass, fragile=fragile, is_rotatebleXYZ=is_rotatableXYZ)]*count)
            for i in range(count):
                boxes.append(Box(size=size, mass=mass, fragile=fragile, is_rotatebleXYZ=is_rotatableXYZ))

        if item['type'] == 'container':
            size = item['size']
            cont = Container(size)



#read_data('input.json')

max_size = 6
for i in range(25):
    boxes.append(Box([random.randint(max_size // 4, max_size) for i in range(3)], 5, False, [False] * 3))

#сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)



box_dict = { box.id:box for box in boxes }

# for ind, box in enumerate(boxes):
#     print('Processing {} of {}'.format(ind+1, len(boxes)))
#     pos = find_place(cont, box, box_dict)
#     if pos is not None:
#         cont.put(box, pos)

length = len(boxes)
ind = 0
packed = [0]*len(boxes)
_boxes = []

print('Packed {} of {}'.format(ind, length))
while boxes:
    box = boxes.pop(0)
    pos = find_place(cont, box, box_dict)
    if pos is not None:
        ind += 1
        _boxes.append(box)
        cont.put(box, pos)
    else:
        packed[box.id] += 1
        if packed[box.id] > 2:
            break
        else:
            boxes.append(box)
    print('Packed {} of {}'.format(ind, length))



write_positions("output.json", _boxes)

new_drawing.draw("output.json", CONT_X, CONT_Y, CONT_Z, _boxes)
