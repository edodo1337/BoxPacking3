import json
import numpy as np
import math
import argparse



def obj2D_functional(box):  # !!!не используется
    k1 = 1
    k2 = 2
    k3 = 1
    S = box.size[0] * box.size[1]
    P = 2 * (box.size[0] + box.size[1])
    return k1 * S + k2 * P


def obj3D_functional(box):  # !!!не используется
    k1 = 1
    k2 = 2
    k3 = 3
    return k1 * box.size[2] + k2 * box.size[0] * box.size[1] * box.size[2]


def find_place(container, box, box_dict, layer_packed):
    #   метод для поиска позиции (первой удачной), в которую можно поместить
    #   коробку. Возвращает позицию [x,y,z], если не найдена - None

    #   цикл по спейсу контейнера, проверяем, если ячейка не занята (None)
    #   и коробка устойчива и помещается, если нет то пытаемся ее
    #   вращать и поместить опять (в ту же точку)

    flag_fit = False
    flag_balanced = False
    cont_x, cont_y, cont_z = container.size
    i = j = k = 0
    while i < cont_z:  # Z
        # if layer_packed[i] == 0:    # если в слое нет заполненных ячеек, пропускаем
        #     #print('Full layer', i)
        #     i += 1
        #     continue
        j = 0
        while j < cont_y:  # Y
            k = 0
            while k < cont_x:  # X
                if container.space[k][j][i] == None:
                    flag_balanced = is_balanced(box, container, [k, j, i])
                    flag_fit = is_fit(box, container, [k, j, i], box_dict)
                    if flag_fit and flag_balanced:
                        for layer in range(i, i + box.size[2]):  # вычитаем свободные ячейки из слоя в который положили
                            layer_packed[layer] -= box.size[0] * box.size[1]
                        return [k, j, i]
                    else:
                        var = 0
                        while not flag_fit or not flag_balanced:
                            if var > 27:  # 3^3
                                k += 1
                                box.load_identity()
                                break
                            box.tryRotations(var)
                            flag_balanced = is_balanced(box, container, [k, j, i])
                            flag_fit = is_fit(box, container, [k, j, i], box_dict)
                            var += 1
                else:
                    #   получаем коробку, которая занимает текущую ячейку и скипаем на величину ее размера по оси Х
                    occupied_size = box_dict[container.space[k][j][i]].diag
                    # i += occupied_size[2]
                    # j += occupied_size[1]
                    k += occupied_size[0]  # по X
            j += 1
        i += 1


    print('---No place size: {} balanced: {}, fit: {}'.format(box.diag, flag_balanced, flag_fit))
    return None


def is_fit(box, container, position, box_dict):
    #   проверяет, может ли коробка поместиться с углом в данной точке (position)
    #   и не пересекает ли при этом дргуие коробки
    #   возвращает True, если норм

    pos_x, pos_y, pos_z = position
    cont_size_x, cont_size_y, cont_size_z = container.size

    #   не выходит ли за пределы контейнера
    if (pos_z + box.diag[2] > cont_size_z) or (pos_y + box.diag[1] > cont_size_y) \
            or (pos_x + box.diag[0] > cont_size_x):
        return False

    if (pos_z + box.diag[2] < 0) or (pos_y + box.diag[1] < 0) or (pos_x + box.diag[0] < 0):
        return False

    #       уже не надо, но пусть останется, чтобы можно было итерировать "назад" (в обратном порядке)
    #       когда отриц. значения вектора диагонали ( типа range(N, M, -1) )
    #       типа так range(pos_x, pos_x + int(box.diag[0] / abs(box.diag[0])) * (1 + abs(box.diag[0])), stepX)

    stepX = int(box.diag[0] / abs(box.diag[0]))  ###     vector / |vector|  - будет 1 или -1
    stepY = int(box.diag[1] / abs(box.diag[1]))
    stepZ = int(box.diag[2] / abs(box.diag[2]))

    #       не пересекает ли другие коробки и нет ли снизу хрупких
    for i in range(pos_z, pos_z + box.diag[2]):  # Z
        if i >= cont_size_z + 1:
            continue
        for j in range(pos_y, pos_y + box.diag[1]):  # Y
            if j >= cont_size_y + 1:
                continue
            for k in range(pos_x, pos_x + box.diag[0]):  # X
                if k >= cont_size_x + 1:
                    continue

                #   чтобы под коробкой не оказалось хрупкой коробки
                if i > 0 and container.space[k][j][i] != None:
                    if box_dict[container.space[k][j][i]].fragile:
                        return False

                try:
                    if container.space[k][j][i] != None:
                        return False
                except Exception as e:
                    print("INDEX ERROR", [k, j, i], str(e))
                    return False

    return True


def is_balanced(box, cont, position):
    #       сбалансированность корокбки. считает, что коробка сбалансирована, если под 4 углами что-то есть
    #       возвращает True, если норм

    pos_x, pos_y, pos_z = position
    if pos_z == 0:
        return True

    centerX, centerY = (box.diag[0] // 2 + pos_x), (box.diag[1] // 2 + pos_y)

    cont_size_x, cont_size_y, cont_size_z = cont.size

    if (centerY > cont_size_y - 1) or (centerY < 0):
        # print('--out of cont')
        return False

    if (centerX > cont_size_x - 1) or (centerX < 0):
        # print('--out of cont')
        return False


    #       проверяет наличие чего-нибудь под 4-мя углами коробки
    x, y, z = position
    try:
        if (cont.space[x][y][z - 1] == None or cont.space[x + box.diag[0] - 1][y][z - 1] == None
                or cont.space[x + box.diag[0] - 1][y + box.diag[1] - 1][z - 1] == None or
                cont.space[x][y + box.diag[1] - 1][z - 1] == None):
            return False
        else:
            return True
    except IndexError:
        return False

    #       то же самое, но с тремя углами
    # r_d = cont.space[x][y][z - 1] == None
    # r_u = cont.space[x + box.size[0] - 1][y][z - 1] == None
    # l_u = cont.space[x + box.size[0] - 1][y + box.size[1] - 1][z - 1] == None
    # l_d = cont.space[x][y + box.size[1] - 1][z - 1] == None
    #
    # if sum([r_d, r_u, l_u, l_d])<3:
    #     return False
    # else True

    ##return False if (cont.space[centerX][centerY][position[2] - 1] == None) else True


def is_intersect(box1, box2, position):  # !!!не используется (пытался определять пересечения 2х коробок)
    pass
#     plane1_XY = [(0, 0), (box1.diag[0], box1.diag[1])]
#     plane1_XZ = [(0, 0), (box1.diag[0], box1.diag[2])]
#     plane1_YZ = [(0, 0), (box1.diag[1], box1.diag[2])]
#
#     plane1_XY = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[0], box1.diag[1])]
#     plane1_XZ = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[0], box1.diag[2])]
#     plane1_YZ = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[1], box1.diag[2])]


def squares_intersect(plane1, plane2):
    #       !!!не используется (пытался определять
    #       пересечения прямоугольников (проекций коробок на плоскости (метод проекций))
    # 1 - 2
    # |   |
    # 0 - 3

    lenX = plane1[3] - plane1[0]
    lenY = plane1[0] - plane1[1]
    if abs(plane1[0] - plane2[0]) < lenX or (abs(plane1[0] - plane2[3])) < lenX:
        return True
    if abs(plane1[0] - plane2[0]) < lenX or (abs(plane1[0] - plane2[1])) < lenY:
        return True

    return False


def write_positions(filename, boxes):  # метод для записи выходных данных в оутпут.джсон
    fout = open(filename, 'w')
    output_list = []
    for box in boxes:
        if box.position == None:
            continue
        for box_dict in box.getattrs():
            output_list.append(box_dict)

    output = json.dumps(output_list)
    #print(output)
    fout.write(output)


def createParser(): # парсер параметров запуска
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='random')
    parser.add_argument('-c', '--count')
    parser.add_argument('-maxs', '--max_size')
    parser.add_argument('-mins', '--min_size')

    return parser


#       матрицы поворота
Rx = np.array(
    [
        [1, 0, 0],
        [0, 0, -1],
        [0, 1, 0]
    ]
)

Ry = np.array(
    [
        [0, 0, 1],
        [0, 1, 0],
        [-1, 0, 0]
    ]
)

Rz = np.array(
    [
        [1, -1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]
)

Qx = np.array(
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, -1, 0]
    ]
)

Qy = np.array(
    [
        [0, 0, -1],
        [0, 1, 0],
        [1, 0, 0]
    ]
)

Qz = np.array(
    [
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 1]
    ]
)

Ident = np.array(
    [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
)
