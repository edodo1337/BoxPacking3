import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import random
from entities import *
import json



########
# Рисование вокселями в matplotlib
#######

def cuboid_data(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]
    # edges = np.array(edges).astype(float)
    # pos = np.array([1,1,1])
    # edges += pos

    return edges


def plotCubeAt(boxes, colors, **kwargs):
    g = []
    for box in boxes:
        g.append(cuboid_data(box))

    return Poly3DCollection(np.concatenate(g),
                            facecolors=np.repeat(colors, 6, axis=0), **kwargs)


def draw(filename, SIZE_X, SIZE_Y, SIZE_Z, boxes):
    fin = open(filename, 'r')
    data = json.load(fin)
    box_data = []

    for i in data:
        pos = tuple(i['position'])
        x_pos = [x0 + x for x0, x in zip(pos, (i['diag'][0], 0, 0))]
        y_pos = [y0 + y for y0, y in zip(pos, (0, i['diag'][1], 0))]
        z_pos = [z0 + z for z0, z in zip(pos, (0, 0, i['diag'][2]))]

        box_data.append([pos, x_pos, y_pos, z_pos])

    #colors = [np.random.rand(3, ) for i in range(len(box_data))]
    colors = []
    for box in boxes:
        if box.position is not None:
            if box.fragile:
                colors.append((0.5, 0.5, 0.5, 0.5))
            else:
                colors.append(np.random.rand(3, ))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    pc = plotCubeAt(box_data, colors=colors, edgecolor="k")
    ax.add_collection3d(pc)
    ax.set_xlim([0, SIZE_X])
    ax.set_ylim([0, SIZE_Y])
    ax.set_zlim([0, SIZE_Z])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

# draw("PackerOUT/public/static/output.json")
