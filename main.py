from entities import *
from utils import *
import json
import new_drawing
import random
import sys
import time

start_time = time.time()

# boxdb = BoxDatabase()
#   размеры контейнера
CONT_X = 6
CONT_Y = 6
CONT_Z = 6

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
            globals()['cont'] = Container(size)
            globals()['CONT_X', 'CONT_Y', 'CONT_Z'] = size[0], size[1], size[2]
# # #

parser = createParser() # для чтения параметров запуска
namespace = parser.parse_args(sys.argv[1:])

#print(namespace)

if namespace.mode == 'file':
    read_data('input.json')

else:   # Рандомный набор коробок
    box_count = 12     # количество коробок
    max_size = 3        # макс размер коробки
    min_size = max_size // 4 if max_size // 4 != 0 else 1   # минимальный разрмер
    #min_size = 1
    for i in range(box_count):
        # is_fragile = (i % (max_size / 15)) == 0 #  каждая 15-я коробка будет хрупкой
        # print('asd', is_fragile)
        #is_rotatebleXYZ = [random.randint(min_size, max_size) % 2 == 0 for j in range(3)]  # рандомизация
        is_rotatebleXYZ = [True]*3
        boxes.append(
            Box([random.randint(min_size, max_size) for j in range(3)], 5, fragile=random.randint(0,100)%3 == 0, is_rotatebleXYZ=is_rotatebleXYZ))

    # for i in range(box_count//5):
    #     boxes.append(Box([random.randint(max_size // 4, max_size // 2) for i in range(3)], 5, True, [False] * 3))



#       сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)

box_dict = { box.id:box for box in boxes }  # словарь для доступа к коробке по ее id
layer_packed = [(cont.size[0] ) * (cont.size[1] )] * (cont.size[2] )  # массив хранит количество свободных ячеек в каждом слое, чтобы через них потом перескакивать


length = len(boxes)
ind = 0
packed = [0]*len(boxes) # состояние коробки по ее id, количество попыток ее упаковать
_boxes = []

print(cont.size)
print(layer_packed)
print('Packed {} of {}'.format(ind, length))

while boxes:  # цикл по коробкам, пытаемся поместить
    box = boxes.pop(0)  # вынимается первая коробка в очереди
    pos = find_place(cont, box, box_dict, layer_packed)
    if pos is not None:
        ind += 1
        _boxes.append(box)
        cont.put(box, pos)
    else:  # если коробка не поместилась она перемещается вниз очереди
        packed[box.id] += 1
        if packed[box.id] > 2:  # если 2 раза коробка не поместилась, значит не судьба
            break
        else:
            boxes.append(box)
    print('Packed {} of {}'.format(ind, length))

print('Program execution time {}'.format(time.time() - start_time))
print(layer_packed)

write_positions("output.json", _boxes)  # запись в файл

new_drawing.draw("output.json", cont.size[0], cont.size[1], cont.size[2], _boxes)
