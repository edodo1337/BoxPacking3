import json
import numpy as np


#       не используется
def obj2D_functional(box):
    k1 = 1
    k2 = 2
    k3 = 1

    S = box.size[0] * box.size[1]
    P = 2 * (box.size[0] + box.size[1])

    return k1 * S + k2 * P


#       не используется
def obj3D_functional(box):
    k1 = 1
    k2 = 2
    k3 = 3

    return k1 * box.size[2] + k2 * box.size[0] * box.size[1] * box.size[2]


def find_place(container, box, box_dict):
    #######
    i = j = k = 0
    while i <= container.size[2]:  # Z
        j = 0
        while j <= container.size[1]:  # Y
            k = 0
            while k <= container.size[0]:  # X
                if container.space[k][j][i] == None:
                    if is_fit(box, container, [k, j, i], box_dict) and is_balanced(box, container, [k, j, i]):
                        return [k, j, i]
                    else:
                        var = 0
                        while not is_fit(box, container, [k, j, i], box_dict) \
                                or not is_balanced(box, container, [k, j, i]):
                            if var > 27:  # 3^3
                                k += 1
                                box.load_identity()
                                break
                            box.tryRotations(var)
                            var += 1
                else:
                    occupied_size = box_dict[container.space[k][j][i]].diag
                    # i += occupied_size[2]
                    # j += occupied_size[1]
                    k += occupied_size[0]
                    # k+=1
            j += 1
        i += 1

    print('---No place', box.size)
    return None

def is_fit(box, container, position, box_dict):
    if (position[2] + box.diag[2] > container.size[2]) or (position[1] + box.diag[1] > container.size[1]) \
            or (position[0] + box.diag[0] > container.size[0]):
        return False

    if (position[2] + box.diag[2] < 0) or (position[1] + box.diag[1] < 0) or (position[0] + box.diag[0] < 0):
        return False

    #       уже не надо, но пусть останется, чтобы можно было итерировать "назад" (в обратном порядке)
    #       когда отриц. значения вектора диагонали

    stepX = int(box.diag[0] / abs(box.diag[0]))
    stepY = int(box.diag[1] / abs(box.diag[1]))
    stepZ = int(box.diag[2] / abs(box.diag[2]))

    for i in range(position[2], position[2] + int(box.diag[2] / abs(box.diag[2])) * (1 + abs(box.diag[2])), stepZ):  # Z
        if i >= container.size[2] + 1:
            continue
        for j in range(position[1], position[1] + int(box.diag[1] / abs(box.diag[1])) * (1 + abs(box.diag[1])),
                       stepY):  # Y
            if j >= container.size[1] + 1:
                continue
            for k in range(position[0], position[0] + int(box.diag[0] / abs(box.diag[0])) * (1 + abs(box.diag[0])),
                           stepX):  # X
                if k >= container.size[0] + 1:
                    continue

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
    if position[2] == 0:
        return True

    centerX, centerY = (box.diag[0] // 2 + position[0]), (box.diag[1] // 2 + position[1])

    if (centerY > cont.size[1] - 1) or (centerY < 0):
        print('--out of cont')
        return False

    if (centerX > cont.size[0] - 1) or (centerX < 0):
        print('--out of cont')
        return False

    x, y, z = position
    if (cont.space[x][y][z - 1] == None or cont.space[x + box.size[0] - 1][y][z - 1] == None
            or cont.space[x + box.size[0] - 1][y + box.size[1] - 1][z - 1] == None or cont.space[x][y + box.size[1] - 1][z - 1] == None):
        return False
    else:
        return  True

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


def is_intersect(box1, box2, position):
    #        не используется
    pass
#     plane1_XY = [(0, 0), (box1.diag[0], box1.diag[1])]
#     plane1_XZ = [(0, 0), (box1.diag[0], box1.diag[2])]
#     plane1_YZ = [(0, 0), (box1.diag[1], box1.diag[2])]
#
#     plane1_XY = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[0], box1.diag[1])]
#     plane1_XZ = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[0], box1.diag[2])]
#     plane1_YZ = [(box1.position[0] - position[0], box1.position[1] - position[1]), (box1.diag[1], box1.diag[2])]


def squares_intersect(plane1, plane2):
    #       не используется
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


def write_positions(filename, boxes):
    fout = open(filename, 'w')
    output_list = []
    for box in boxes:
        if box.position == None:
            continue
        for box_dict in box.getattrs():
            output_list.append(box_dict)

    output = json.dumps(output_list)
    print(output)
    fout.write(output)


def makeStack(boxes):
    pass


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
        [0, -1, 0],
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
