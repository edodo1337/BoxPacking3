import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import random
from entities import *
import json





def draw(filename):
    fin = open(filename, 'r')
    data = json.load(fin)
    boxes = []

    for i in data:
        pos = tuple(i['position'])
        x_pos = [x0 + x for x0, x in zip(pos, (i['diag'][0], 0, 0))]
        y_pos = [y0 + y for y0, y in zip(pos, (0, i['diag'][1], 0))]
        z_pos = [z0 + z for z0, z in zip(pos, (0, 0, i['diag'][2]))]

        boxes.append([pos, x_pos, y_pos, z_pos])

    colors = [np.random.rand(3, ) for i in range(len(boxes))]
