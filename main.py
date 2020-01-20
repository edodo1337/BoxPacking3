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
CONT_X = 15
CONT_Y = 15
CONT_Z = 15

cont = Container([CONT_X, CONT_Y, CONT_Z])
boxes = []


def read_data(filename):
    #       чтение данных из файла
    f = open(filename, "r").read()
    f_json = json.loads(f)
    for item in f_json:
        # print(item)
        if item['type'] == 'box':
            size = item['size']
            mass = item['mass']
            fragile = item['fragile']
            is_rotatableXYZ = item['is_rotatableXYZ']
            count = item['count']
            # boxes.extend([Box(size=size, mass=mass, fragile=fragile, is_rotatebleXYZ=is_rotatableXYZ)]*count)
            for i in range(count):
                boxes.append(Box(size=size, mass=mass, fragile=fragile, is_rotatebleXYZ=is_rotatableXYZ))

        if item['type'] == 'container':
            size = item['size']
            globals()['cont'] = Container(size)
            globals()['CONT_X', 'CONT_Y', 'CONT_Z'] = size[0], size[1], size[2]


# # #

parser = createParser()  # для чтения параметров запуска
namespace = parser.parse_args(sys.argv[1:])

# print(namespace)

if namespace.mode == 'file':
    read_data('input.json')

else:  # Рандомный набор коробок
    box_count = 100  # количество коробок
    max_size = 5  # макс размер коробки
    min_size = max_size // 4 if max_size // 4 != 0 else 1  # минимальный разрмер
    # min_size = 1
    for i in range(box_count):
        is_rotatebleXYZ = [random.randint(min_size, max_size) % 2 == 0 for j in range(3)]  # рандомизация
        #is_rotatebleXYZ = [True] * 3
        box_fragile = random.randint(0, 100) % 12 == 1
        box_size = [random.randint(min_size, max_size) for j in range(3)]
        box_mass = box_size[0] * box_size[1] * box_size[2] / (2 if box_fragile else 1)
        boxes.append(
            Box(size=box_size, mass=box_mass, fragile=box_fragile, is_rotatebleXYZ=is_rotatebleXYZ))

#       сортировка по размеру
boxes.sort(key=lambda x: x.size[0] * x.size[1] * x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0] * x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)

box_dict = {box.id: box for box in boxes}  # словарь для доступа к коробке по ее id
layer_packed = [(cont.size[0]) * (cont.size[1])] * (
cont.size[2])  # массив хранит количество свободных ячеек в каждом слое, чтобы через них потом перескакивать

length = len(boxes)
ind = 0
packed = [0] * len(boxes)  # состояние коробки по ее id, количество попыток ее упаковать
_boxes = []

# print('Layer packed:', layer_packed)
# print('Packed {} of {}'.format(ind, length))

center_of_mass = [0, 0, 0]  # X, Y, Z (центр тяжести общий)
sum_mass = 0  # суммарная масса коробок

proection_X = []
proection_Y = []
proection_Z = []
# put_boxes = []

while boxes:  # цикл по коробкам, пытаемся поместить
    box = boxes.pop(0)  # вынимается первая коробка в очереди
    pos = find_place(cont, box, box_dict, layer_packed, proection_X, proection_Y, proection_Z, _boxes)
    if pos is not None:
        proection_X.append([pos[0], pos[0] + box.size[0]])
        proection_Y.append([pos[1], pos[1] + box.size[1]])
        proection_Z.append([pos[2], pos[2] + box.size[2]])
        center_of_mass = [
            (center_of_mass[0] * sum_mass + box.mass * (pos[0] + box.diag[0] / 2)) / (sum_mass + box.mass),
            (center_of_mass[1] * sum_mass + box.mass * (pos[1] + box.diag[1] / 2)) / (sum_mass + box.mass),
            (center_of_mass[2] * sum_mass + box.mass * (pos[2] + box.diag[2] / 2)) / (sum_mass + box.mass)
        ]
        sum_mass += box.mass

        ind += 1
        _boxes.append(box)
        # put_boxes.append(box)
        cont.put(box, pos)
    else:  # если коробка не поместилась она перемещается в конец очереди
        packed[box.id] += 1
        if packed[box.id] > 2:  # если 2 раза коробка не поместилась, значит не судьба
            break
        else:
            boxes.append(box)
    print('Packed {} of {}'.format(ind, length))

print('Program execution time {}'.format(time.time() - start_time))
print('Layer packed:', layer_packed)
print('Center of mass:', [round(i, 2) for i in center_of_mass],     # центр тяжести фактический
      'Should be at:', [CONT_X / 2, CONT_Y / 2, CONT_Z / 2],        # центр тяжести идеальный
      'Deviation:', [round((i - j / 2) * 2 / j, 2) for i, j in zip(center_of_mass, cont.size)]) # относительное отклонение
# print('Cont.space', cont.space)
# print('Cont.space_free', cont.space_point)

write_positions("output.json", _boxes)  # запись в файл

new_drawing.draw("output.json", cont.size[0], cont.size[1], cont.size[2], _boxes)
