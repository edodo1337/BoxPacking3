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


def find_place(container, box, box_dict, layer_packed, proect_x, proect_y, proect_z, put_boxes):
    #   метод для поиска позиции (первой удачной), в которую можно поместить
    #   коробку. Возвращает позицию [x,y,z], если не найдена - None

    #   цикл по спейсу контейнера, проверяем, если ячейка не занята (None)
    #   и коробка устойчива и помещается, если нет то пытаемся ее
    #   вращать и поместить опять (в ту же точку)

    flag_fit = False
    flag_fit_n = False
    flag_balanced = False
    cont_x, cont_y, cont_z = container.size

    i = j = k = 0
    while i < cont_z:  # Z
        bsize_x, bsize_y, bsize_z = box.size
        # если в слое недостаточно свободного места, пропускаем
        count_empty_block = layer_packed[i]
        if count_empty_block < bsize_x*bsize_y and count_empty_block < bsize_x*bsize_z and count_empty_block < bsize_z*bsize_y:
            #print('Full layer', i)
            i += 1
            continue
        j = 0
        while j < cont_y:  # Y
            k = 0
            while k < cont_x:  # X
                point = container.space[k][j][i]
                if point == None:
                    flag_balanced = is_balanced(box, container, [k, j, i], box_dict)
                    # flag_fit = is_fit(box, container, [k, j, i], box_dict)
                    flag_fit_n = is_fit_new(box, container, [k, j, i], box_dict, proect_x, proect_y, proect_z, put_boxes)
                    if flag_fit_n and flag_balanced:
                        bsize_x, bsize_y, bsize_z = box.size
                        for layer in range(i, i + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
                            layer_packed[layer] -= bsize_x * bsize_y

                        return [k, j, i]
                    else:
                        var = 0
                        while not flag_fit_n or not flag_balanced:
                            if var > 27:  # 3^3
                                k += 1
                                box.load_identity()
                                break
                            box.tryRotations(var)
                            flag_balanced = is_balanced(box, container, [k, j, i], box_dict)
                            flag_fit_n = is_fit_new(box, container, [k, j, i], box_dict, proect_x, proect_y, proect_z, put_boxes)
                            # flag_fit = is_fit(box, container, [k, j, i], box_dict)
                            if flag_fit_n and flag_balanced:
                                bsize_x, bsize_y, bsize_z = box.size
                                for layer in range(i, i + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
                                    layer_packed[layer] -= bsize_x * bsize_y
                                return [k, j, i]
                            var += 1
                else:
                    #   получаем коробку, которая занимает текущую ячейку и скипаем на величину ее размера по оси Х
                    occupied_size = box_dict[point].diag
                    # i += occupied_size[2]
                    # j += occupied_size[1]
                    k += occupied_size[0]  # по X
            j += 1
        i += 1

    print('---No place size: {} balanced: {}, fit: {}'.format(box.diag, flag_balanced, flag_fit_n))
    return None

def is_fit_new(box, container, position, box_dict, proections_x, proections_y, proections_z, put_boxes):
    pos_x, pos_y, pos_z = position
    cont_size_x, cont_size_y, cont_size_z = container.size
    box_x, box_y, box_z = box.size
    #   не выходит ли за пределы контейнера
    if (pos_z + box.diag[2] > cont_size_z) or (pos_y + box.diag[1] > cont_size_y) \
            or (pos_x + box.diag[0] > cont_size_x):
        return False
    if (pos_z + box.diag[2] < 0) or (pos_y + box.diag[1] < 0) or (pos_x + box.diag[0] < 0):
        return False
    #       !!!не пересекает ли другие коробки и нет ли снизу хрупких
    #       Способ проекций через отрезки:
    # for i in range(0, len(proections_x)):
    #     x = proections_x[i]
    #     y = proections_y[i]
    #     z = proections_z[i]
    #     # print('1 x', x[0], pos_x, x[1], 'y', y[0], pos_y, y[1], 'z', z[0], pos_z, z[1])
    #     # print('2 x', x[0], pos_x + box_x, x[1], 'y', y[0], pos_y + box_y, y[1], 'z', z[0], pos_z + box_z, z[1])
    #     if x != None:
    #         if x[0] <= pos_x < x[1] or x[0] < pos_x + box_x <= x[1]:
    #             if y[0] <= pos_y < y[1] or y[0] < pos_y + box_y <= y[1]:
    #                 if z[0] <= pos_z < z[1] or z[0] < pos_z + box_z <= z[1]:
    #                     return False
    #         elif pos_x <= x[0] and pos_x + box_x >= x[1] and pos_y <= y[0] and pos_y + box_y >= y[1] and pos_z <= z[0] and pos_z + box_z >= z[1]:
    #             return False

          # !!!не пересекает ли другие коробки и нет ли снизу хрупких
          # Способ проекций:
    if put_boxes != []:
        for select_box in put_boxes:
            x, y, z = select_box.size
            px, py, pz = select_box.position

            check_xy = check_rectangle([pos_x, pos_y], [pos_x + box_x, pos_y + box_y], [px, py], [px + x, py + y])  # XY
            check_xz = check_rectangle([pos_x, pos_z], [pos_x + box_x, pos_z + pos_z], [px, pz], [px + x, pz + z])  # XZ
            check_yz = check_rectangle([pos_y, pos_z], [pos_y + box_y, pos_z + pos_z], [py, pz], [py + y, pz + z])  # YZ

            if (not check_xy) and (not check_xz) and (not check_yz):
                return False
    return True

def check_rectangle(pos1, diag1, pos2, diag2):
    # проверка перывх проекций
    if (pos1[0] <= pos2[0] < diag1[0]) or (pos1[0] < diag2[0] <= diag1[0]) \
            or (pos2[0] <= pos1[0] < diag2[0]) or (pos2[0] < diag1[0] <= diag2[0]):
        # проверка вторых проекций
        if (pos1[1] <= pos2[1] < diag1[1]) or (pos1[1] < diag2[1] <= diag1[1]) \
                or (pos2[1] <= pos1[1] < diag2[1]) or (pos2[1] < diag1[1] <= diag2[1]):
            return False
    return True


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
                fragile = is_fragile(container, box_dict, k, j, i)
                if not fragile:
                    return False

    #       !!!не пересекает ли другие коробки и нет ли снизу хрупких
    #       Способ проекций:
    #       !!!не пересекает ли другие коробки и нет ли снизу хрупких
    #       проверять только поверхность коробки:
    # print(container.space_point)
    # if [k, j, i] in container.space_point:
    #     print('False')
    # if i > 0 and container.space[k][j][i - 1] != None:
    #     if box_dict[container.space[k][j][i - 1]].fragile:
    #         return False
    return True

#   чтобы под коробкой не оказалось хрупкой коробки
def is_fragile(container, box_dict, k, j, i):
    if i > 0 and container.space[k][j][i - 1] != None:
        if box_dict[container.space[k][j][i - 1]].fragile:
            return False
    if container.space[k][j][i] != None:
        return False
    return True

def is_balanced(box, cont, position, box_dict):
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
        elif box_dict[cont.space[x][y][z - 1]].fragile:
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
