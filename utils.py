import json
import entities

def obj2D_functional(box):
    k1 = 1
    k2 = 1
    k3 = 1

    S = box.size[0] * box.size[1]
    P = 2 * (box.size[0] + box.size[1])

    return k1*S

def obj3D_functional(box):
    k1 = 1
    k2 = 2
    k3 = 3

    return k1*box.size[2] + k2*box.size[0]*box.size[1]*box.size[2]

def find_place(container, box):
    rotation = 1
    for i in range(container.size[2]):  # Z
        for j in range(container.size[1]):  # Y
            for k in range(container.size[0]):  # X
                if container.space[k][j][i] == None:
                    while (not is_fit(box, container, [k,j,i])) or (rotation>24):
                        tryRotations(box, rotation)
                        rotation+=1


                    if is_fit(box, container, [k, j, i]):
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


def tryRotations(box, var):
    rotations = {
        '0': box.load_identity,
        '1': box.rotateX(),
        '2': box.rotateY(),
        '3': box.rotateZ(),
    }
    counter = 0
    for i in rotations.keys():
        for j in rotations.keys():
            for k in rotations.keys():
                if counter>var:
                    break
                else:
                    rotations[i]
                    rotations[j]
                    rotations[k]

def write_positions(boxdb, filename):
    fout = open(filename, 'w')
    output_list = []
    output_dict = {}

    for box in boxdb.box_list:
        output_dict['size'] = box.size
        output_dict['position'] = [ box.position[0] + box.size[0] // 2,
                               box.position[1] + box.size[1] // 2,
                               box.position[2] + box.size[2] // 2
                               ]
        output_list.append(output_dict)

    output = json.dumps(output_list)
    print(output)
    fout.write(output)
