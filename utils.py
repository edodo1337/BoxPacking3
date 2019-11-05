import json
import entities

def obj2D_functional(box):
    k1 = 1
    k2 = 2
    k3 = 1

    S = box.size[0] * box.size[1]
    P = 2 * (box.size[0] + box.size[1])

    return k1*S + k2*P

def obj3D_functional(box):
    k1 = 1
    k2 = 2
    k3 = 3

    return k1*box.size[2] + k2*box.size[0]*box.size[1]*box.size[2]

def find_place(container, box):
    for i in range(container.size[2]):  # Z
        for j in range(container.size[1]):  # Y
            for k in range(container.size[0]):  # X
                if container.space[k][j][i] == None:
                    rotation = 1

                    while (not is_fit(box, container, [k, j, i])) and (rotation < 24):
                        print(box.size)
                        box.tryRotations(rotation)
                        rotation += 1

                    if is_fit(box, container, [k, j, i]) and is_balanced(box, container, [k, j, i]):
                        return [k, j, i]

    return None


def is_fit(box, container, position):
    if (container.size[2] - box.size[2] - position[2] - 1) < 0:
        return False
    elif (container.size[1] - box.size[1] - position[1] - 1) < 0:
        return False
    elif (container.size[0] - box.size[0] - position[0] - 1) < 0:
        return False


    for i in range(position[2], position[2] + box.size[2]):  # Z
        for j in range(position[1], position[1] + box.size[1]):  # Y
            for k in range(position[0], position[0] + box.size[0]):  # X
                if container.space[k][j][i] != None:
                    return False

    return True



def write_positions(boxdb, filename):
    fout = open(filename, 'w')
    output_list = []


    for box in boxdb.box_list:
        if box.position!=None:
            output_dict = {}
            output_dict['size'] = box.size
            output_dict['position'] = [ box.position[0] + box.size[0] / 2,
                                   box.position[1] + box.size[1] / 2,
                                   box.position[2] + box.size[2] / 2
                                   ]
            output_list.append(output_dict)
            output = json.dumps(output_list)

    print(output)
    fout.write(output)

def is_balanced(box, cont, position):
    if position[2] == 0:
        return True

    centerX, centerY = (position[0] + box.size[0]) // 2, (position[1] + box.size[1]) // 2

    return False if (cont[centerX, centerY, position[2] - 1] == None) else True

