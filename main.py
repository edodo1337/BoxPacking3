from entities import *
from utils import *
import json
import new_drawing


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



read_data('input.json')

# max_size = 6
# for i in range(5):
#     boxes.append(Box([random.randint(max_size // 4, max_size) for i in range(3)], 5, [False], [True] * 3))


#сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)



box_dict = { box.id:box for box in boxes }

for ind, box in enumerate(boxes):
    print('Processing {} of {}'.format(ind, len(boxes)))
    pos = find_place(cont, box, box_dict)
    if pos is not None:
        cont.put(box, pos)


write_positions("output.json", boxes)

new_drawing.draw("output.json", CONT_X, CONT_Y, CONT_Z, boxes)
