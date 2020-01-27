import json
import numpy as np
import math
import argparse



def obj2D_functional(box):  # !!!не использу`1ется
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


# def find_place(container, box, box_dict, layer_packed, put_boxes):
#     #   метод для поиска позиции (первой удачной), в которую можно поместить
#     #   коробку. Возвращает позицию [x,y,z], если не найдена - None
#
#     #   цикл по спейсу контейнера, проверяем, если ячейка не занята (None)
#     #   и коробка устойчива и помещается, если нет то пытаемся ее
#     #   вращать и поместить опять (в ту же точку)
#     # find_point(container, box, box_dict, layer_packed, put_boxes)
#     flag_fit = False
#     flag_balanced = False
#     cont_x, cont_y, cont_z = container.size
#
#     i = j = k = 0
#     while i < cont_z:  # Z
#         bsize_x, bsize_y, bsize_z = box.size
#         # если в слое недостаточно свободного места, пропускаем
#         count_empty_block = layer_packed[i]
#         if count_empty_block < bsize_x*bsize_y and count_empty_block < bsize_x*bsize_z and count_empty_block < bsize_z*bsize_y:
#             #print('Full layer', i)
#             i += 1
#             continue
#         j = 0
#         while j < cont_y:  # Y
#             k = 0
#             while k < cont_x:  # X
#                 point = container.space[k][j][i]
#                 if point == None:
#                     # flag_balanced = is_balanced(box, container, [k, j, i], box_dict)
#                     # flag_fit = is_fit(box, container, [k, j, i], box_dict)
#                     flag_fit = is_fit_new(box, container, [k, j, i], box_dict, put_boxes)
#                     if not flag_fit:
#                         print('NOT FIT')
#                     if flag_fit :
#                         bsize_x, bsize_y, bsize_z = box.size
#                         for layer in range(i, i + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
#                             layer_packed[layer] -= bsize_x * bsize_y
#
#                         return [k, j, i]
#                     else:
#                         var = 0
#                         while not flag_fit:
#                             if var > 27:  # 3^3
#                                 k += 1
#                                 box.load_identity()
#                                 break
#                             box.tryRotations()
#                             print(box.rotation_state)
#                             # flag_balanced = is_balanced(box, container, [k, j, i], box_dict)
#                             # flag_fit = is_fit(box, container, [k, j, i], box_dict)
#                             flag_fit = is_fit_new(box, container, [k, j, i], box_dict, put_boxes)
#                             if flag_fit :
#                                 bsize_x, bsize_y, bsize_z = box.size
#                                 for layer in range(i, i + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
#                                     layer_packed[layer] -= bsize_x * bsize_y
#                                 return [k, j, i]
#                             var += 1
#                 else:
#                     #   получаем коробку, которая занимает текущую ячейку и скипаем на величину ее размера по оси Х
#                     occupied_size = box_dict[point].diag
#                     # i += occupied_size[2]
#                     # j += occupied_size[1]
#                     k += occupied_size[0]  # по X
#             j += 1
#         i += 1
#
#     print('---No place size: {} balanced: {}, fit: {}'.format(box.diag, flag_balanced, flag_fit))
#     return None

def find_point(container, box, box_dict, layer_packed, put_boxes):
    #   Стоит делить все пространство контейнера на части (возможно по 50 т.к. контейнер меньше 100 не может быть)
    #   ели св пр-во на данном уровне в данном секторе закончилось, удаляем все, в нем находящиеся точки
    cont_points = container.points
    #cont_points.sort(key=lambda cont_points: cont_points[0] + cont_points[1] + 1000*cont_points[2], reverse=False)
    cont_points.sort(key=lambda cont_points: 10*cont_points[0] + cont_points[1], reverse=False)
    # print(cont_points)
    flag_fit = False
    bsize_x, bsize_y, bsize_z = box.size


    cur_p = 0
    cur_z = cont_points[cur_p][2]
    next_z = cur_z + 100000
    next_p = None

    i=0

    # for point in cont_points:
    #     flag_fit = \
    #         is_fit_new(box, container, point, box_dict, put_boxes)
    #     while flag_fit or box.rotation_state>=27:
    #         if flag_fit:
    #             bsize_x, bsize_y, bsize_z = box.size
    #             # for layer in range(point[2], point[2] + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
    #             #     layer_packed[layer] -= bsize_x * bsize_y
    #             # container.points.remove(point)
    #             container.points = remove_point(cont_points, box, point, box_dict)
    #
    #             # if point[0] + bsize_x < container.size[0]:
    #             #     container.points.append([point[0] + bsize_x, point[1], point[2]])
    #             # if point[1] + bsize_y < container.size[1] or point[0] + bsize_x < container.size[0]:
    #             #     container.points.append([point[0] + bsize_x, point[1] + bsize_y, point[2]])
    #             # if point[1] + bsize_y < container.size[1]:
    #             #     container.points.append([point[0], point[1] + bsize_y, point[2]])
    #             if point[2] + bsize_z < container.size[2]:
    #                 container.points.append([point[0], point[1], point[2] + bsize_z])
    #                 container.put_in_area([point[0], point[1], point[2] + bsize_z], box)
    #
    #             #
    #             # min_box = None
    #             # for box in put_boxes:
    #
    #             container.points.append([point[0] + bsize_x, point[1], point[2]])
    #             container.points.append([point[0] + bsize_x, point[1] + bsize_y, point[2]])
    #             container.points.append([point[0], point[1] + bsize_y, point[2]])
    #             # container.points.append([point[0], point[1], point[2] + bsize_z])
    #
    #             container.put_in_area([point[0] + bsize_x, point[1], point[2]], box)
    #             container.put_in_area([point[0] + bsize_x, point[1] + bsize_y, point[2]], box)
    #             container.put_in_area([point[0], point[1] + bsize_y, point[2]], box)
    #
    #             return point
    #
    #         else:
    #             box.tryRotations()
    #
    # print('---No place size: {}, fit: {}'.format(box.diag, flag_fit))
    # return None


    while i < len(cont_points):
        point = cont_points[i]
        #print('Point', i, cur_z, point[2])
        if point[2] > cur_z:
            if point[2] < next_z:
                next_z = point[2]
                next_p = i
        else:
            pass
            # print('asd')

        count_empty_block = layer_packed[point[2]]

        flag_fit =\
            is_fit_new(box, container, point, box_dict, put_boxes)
        if flag_fit:
            bsize_x, bsize_y, bsize_z = box.size
            # for layer in range(point[2], point[2] + bsize_z):  # вычитаем свободные ячейки из слоя в который положили
            #     layer_packed[layer] -= bsize_x * bsize_y
            # container.points.remove(point)
            container.points = remove_point(cont_points, box, point, box_dict)

            # if point[0] + bsize_x < container.size[0]:
            #     container.points.append([point[0] + bsize_x, point[1], point[2]])
            # if point[1] + bsize_y < container.size[1] or point[0] + bsize_x < container.size[0]:
            #     container.points.append([point[0] + bsize_x, point[1] + bsize_y, point[2]])
            # if point[1] + bsize_y < container.size[1]:
            #     container.points.append([point[0], point[1] + bsize_y, point[2]])
            if point[2] + bsize_z < container.size[2]:
                container.points.append([point[0], point[1], point[2] + bsize_z])
                container.put_in_area([point[0], point[1], point[2] + bsize_z], box)

            #
            # min_box = None
            # for box in put_boxes:


            container.points.append([point[0] + bsize_x, point[1], point[2]])
            container.points.append([point[0] + bsize_x, point[1] + bsize_y, point[2]])
            container.points.append([point[0], point[1] + bsize_y, point[2]])
            # container.points.append([point[0], point[1], point[2] + bsize_z])

            container.put_in_area([point[0] + bsize_x, point[1], point[2]], box)
            container.put_in_area([point[0] + bsize_x, point[1] + bsize_y, point[2]], box)
            container.put_in_area([point[0], point[1] + bsize_y, point[2]], box)


            return point

        else:
            if box.rotation_state>=27:
                box.rotation_state = 0
                box.load_identity()
                if next_p is not None:
                    cur_p = next_p
                    cur_z = cont_points[cur_p][2]
                    next_z = cur_z + 100000
                    next_p = None
                else:
                    if i == len(cont_points) - 1:
                        return None
                    else:
                        pass
                        #print(i, cont_points)
            else:
                if i==next_p:
                    i = cur_p
                    box.tryRotations()
                else:
                    i+=1


    #print('Find point:', False, i, len(cont_points))
    print('---No place size: {}, fit: {}'.format(box.diag,  flag_fit))
    return None

def remove_point(cont_points, box, position, put_boxes):
    bx, by, bz = box.size
    px, py, pz = position
    #    вершины коробки
    box_points = [[px, py, pz], [px + bx, py, pz], [px + bx, py + by, pz], [px, py + by, pz],
                  [px, py + by, pz + bz], [px + bx, py + by, pz + bz], [px + bx, py, pz + bz], [px, py, pz + bz]]
    #   грани коробки, первая вершина всегда ближе к началу координат
    box_face = [[box_points[0], box_points[1]], [box_points[0], box_points[3]], [box_points[0], box_points[7]],
                [box_points[1], box_points[2]], [box_points[3], box_points[2]], [box_points[2], box_points[5]],
                [box_points[7], box_points[4]], [box_points[7], box_points[6]],
                [box_points[6], box_points[5]], [box_points[4], box_points[5]]]
    # points = cont_points
    for c_point in cont_points:
        for face in box_face:
            check = check_section(c_point, face[0], face[1])
            if check:
                # if not (check_space([c_point[0] + 1, c_point[0] + 1], put_boxes)
                #         and check_space([c_point[0] + 1, c_point[0] - 1], put_boxes)
                #         and check_space([c_point[0] - 1, c_point[0] - 1], put_boxes)
                #         and check_space([c_point[0] - 1, c_point[0] + 1], put_boxes)):
                #     if c_point in cont_points:
                #         cont_points.remove(c_point)
                #         #continue
                # # else:
                # #     print(c_point)
                # #     print(cont_points)
                # #     continue
                check1, check2, check3, check4 = False, False, False, False
                if not put_boxes:
                    for select_box in put_boxes:
                        if select_box.position[2] <= c_point < select_box.position[2] + select_box.size[2]:
                            px, py, pz = select_box.position
                            if is_balans([c_point[0] + 1, c_point[0] + 1], [px, py],
                                         [px + select_box.size[0], py + select_box.size[1]]):
                                check1 = True
                            if is_balans([c_point[0] + 1, c_point[0] - 1], [px, py],
                                         [px + select_box.size[0], py + select_box.size[1]]):
                                check2 = True
                            if is_balans([c_point[0] - 1, c_point[0] - 1], [px, py],
                                         [px + select_box.size[0], py + select_box.size[1]]):
                                check3 = True
                            if is_balans([c_point[0] - 1, c_point[0] + 1], [px, py],
                                         [px + select_box.size[0], py + select_box.size[1]]):
                                check4 = True
                        if check1 and check2 and check3 and check4:
                            if c_point in cont_points:
                                cont_points.remove(c_point)

    return cont_points


def check_space(point, put_boxes):
    if point[0] < 0 and point[1] < 0:
        return False
    if not put_boxes:
        for box in put_boxes:
            point_b = box.position
            point_d = [point_b[0] + box.diag[0], point_b[1] + box.diag[1], point_b[2] + box.diag[2]]
            if is_balans(point, point_b, point_d):
                return False



def is_fit_new(box, container, position, box_dict, put_boxes):
    pos_x, pos_y, pos_z = position
    cont_size_x, cont_size_y, cont_size_z = container.size
    box_x, box_y, box_z = box.size
    #   не выходит ли за пределы контейнера
    if (pos_z + box.diag[2] > cont_size_z) or (pos_y + box.diag[1] > cont_size_y) \
            or (pos_x + box.diag[0] > cont_size_x):
        return False

    if (pos_z + box.diag[2] <= 0) or (pos_y + box.diag[1] <= 0) or (pos_x + box.diag[0] <= 0):
        return False
    # point5 - центр
    # point6, point7 - доп точки (использовались для хрпких кообок)
    point1 = point2 = point3 = point4 = point5 = point6 = point7 = False
    if pos_z == 0:
        point1 = point2 = point3 = point4 = point5 = point6 = point7 = True

    # не пересекает ли другие коробки и нет ли снизу хрупких
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
            # нет ли вверху коробки, когда ставим хрупкую
            if box.fragile and pos_z + box_z == pz and not check_xy:
                return False
            if pz + z == pos_z:
                # нет ли внизу хрупкой коробки
                if select_box.fragile:
                    if not check_xy:
                        return False
                else:
                    # стоят ли углы на других коробках
                    if not point1:
                        point1 = is_balans([pos_x + 0.1, pos_y + 0.1], [px, py], [px + x, py + y])
                    if not point2:
                        point2 = is_balans([pos_x + 0.1, pos_y + box_y - 0.1], [px, py], [px + x, py + y])
                    if not point3:
                        point3 = is_balans([pos_x + box_x - 0.1, pos_y + box_y - 0.1], [px, py], [px + x, py + y])
                    if not point4:
                        point4 = is_balans([pos_x + box_x - 0.1, pos_y + 0.1], [px, py], [px + x, py + y])
                    if not point5:
                        point5 = is_balans([pos_x + box_x / 2, pos_y + box_y / 2], [px, py], [px + x, py + y])

    #                 if box.fragile:
    #                     if not point6:
    #                         point6 = is_balans2([pos_x + box_x * 3 / 4, pos_y + box_y / 4], [px, py], [px + x, py + y])
    #                     if not point7:
    #                         point7 = is_balans2([pos_x + box_x / 4, pos_y + box_y * 3 / 4], [px, py], [px + x, py + y])
    # if box.fragile:
    #     if not point6 or not point7:
    #         return False
    if not point1 or not point2 or not point3 or not point4 or not point5:
        return False
    return True

def is_balans(pos1, pos2, diag2):
    # проверка на принадлежность точки прямоугольнику
    if (pos2[0] < pos1[0] < diag2[0]):
        if (pos2[1] < pos1[1] < diag2[1]):
            return True
    return False

def check_section(point, section1, section2):
    if section1[0] == section2[0] and point[0] == section1[0]:
        if section1[1] == section2[1] and point[1] == section1[1]:  # (ху, z изм) линия вертикальна, х неизменяется (все вертикальные грани)
            if section1[2] <= point[2] <= section2[2]:
                return True
        elif section1[2] == section2[2] and point[2] == section1[2]:    # (xz, у изм) линия горизонтальна, х неизменяется
            if section1[1] <= point[1] <= section2[1]:
                return True
    elif section1[1] == section2[1] and section1[2] == section2[2] and \
            point[1] == section1[1] and point[2] == section1[2]: # линия горизонтальна, х изменяется
        if section1[0] <= point[0] <= section2[0]:
            return True
    return False

def check_rectangle(pos1, diag1, pos2, diag2):
    # проверка пересейчения двух прямоугольников
    # проверка перывх проекций
    if (pos1[0] <= pos2[0] < diag1[0]) or (pos1[0] < diag2[0] <= diag1[0]) \
            or (pos2[0] <= pos1[0] < diag2[0]) or (pos2[0] < diag1[0] <= diag2[0]):
        # проверка вторых проекций
        if (pos1[1] <= pos2[1] < diag1[1]) or (pos1[1] < diag2[1] <= diag1[1]) \
                or (pos2[1] <= pos1[1] < diag2[1]) or (pos2[1] < diag1[1] <= diag2[1]):
            return False
    return True



def is_balanced(box, cont, position, box_dict):     # !!! старая версия
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
        # использовалось при уходе от перебора массива конт. в fit
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

def is_fit(box, container, position, box_dict):  # !!! старая версия
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
