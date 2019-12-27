from entities import *
from utils import *
import json
import new_drawing
import random
import sys

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



# # #

parser = createParser() # для чтения параметров запуска
namespace = parser.parse_args(sys.argv[1:])

#print(namespace)

if namespace.mode == 'file':
    read_data('input.json')

else:
    box_count = 100  # количество коробок
    max_size = 5    # макс размер коробки
    min_size = max_size // 4 if max_size // 4 != 0 else 1   # минимальный разрмер
    for i in range(box_count):
        # is_fragile = (i % (max_size / 15)) == 0 #  каждая 15-я коробка будет хрупкой
        # print('asd', is_fragile)
        is_rotatebleXYZ = [random.randint(min_size, max_size) % 2 == 0 for j in range(3)]  # рандомизация
        #print(is_rotatebleXYZ)
        boxes.append(
            Box([random.randint(min_size, max_size) for j in range(3)], 5, fragile=False, is_rotatebleXYZ=is_rotatebleXYZ))

    # for i in range(box_count//5):
    #     boxes.append(Box([random.randint(max_size // 4, max_size // 2) for i in range(3)], 5, True, [False] * 3))



#       сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)

box_dict = { box.id:box for box in boxes }  # словарь для доступа к коробке по ее id

length = len(boxes)
ind = 0
packed = [0]*len(boxes) # состояние коробки по ее id, количество попыток ее упаковать
_boxes = []

print('Packed {} of {}'.format(ind, length))

while boxes:  # цикл по коробкам, пытаемся поместить
    box = boxes.pop(0)  # вынимается первая коробка в очереди
    pos = find_place(cont, box, box_dict)
    if pos is not None:
        ind += 1
        _boxes.append(box)
        cont.put(box, pos)
    else:  # если коробка не поместилась она перемещается вниз очереди
        packed[box.id] += 1
        if packed[box.id] > 4:  # если 4 раза коробка не поместилась, значит не судьба
            break
        else:
            boxes.append(box)
    print('Packed {} of {}'.format(ind, length))


write_positions("output.json", _boxes)

new_drawing.draw("output.json", CONT_X, CONT_Y, CONT_Z, _boxes)
