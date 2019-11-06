#BOX_COUNTER = 0
import numpy as np
from utils import Rx, Ry, Rz

class BoxDatabase():
    def __init__(self):
        self.items = dict()
        self.box_list = []
        self.BOX_COUNTER = 0

    def put(self, *args):
        for item in args:
            self.BOX_COUNTER += 1
            self.items[str(self.BOX_COUNTER)] = item
            self.box_list.append(item)
            item.id = self.BOX_COUNTER

    def get(self, id):
        return self.items.get(str(id))

    def pop(self, id):
        self.items[str(id)] = None

# class AbastractContainer:
#     def __init__(self, size):
#         self.size = size
#         self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]

class AbstractBox:
    def __init__(self, size, is_rotatableXYZ):
        #global BOX_COUNTER
        #BOX_COUNTER += 1
        #self.id = BOX_COUNTER
        self.size = size
        self.default_size = size[:]
        self.position = None
        self.is_rotatableX = is_rotatableXYZ[0]
        self.is_rotatableY = is_rotatableXYZ[1]
        self.is_rotatableZ = is_rotatableXYZ[2]

    def load_identity(self):
        self.size = self.default_size[:]

    def rotateX(self):
        self.size[1], self.size[2] = self.size[2], self.size[1]

    def rotateY(self):
        self.size[0], self.size[2] = self.size[2], self.size[0]

    def rotateZ(self):
        self.size[0], self.size[1] = self.size[1], self.size[0]

    def tryRotations(self, var):
        a = lambda: None
        rotations = {
            '0': a,
            '1': self.rotateX,
            '2': self.rotateY,
            '3': self.rotateZ,
        }
        done = False
        counter = 0

        for i in rotations.keys():
            if done:
                break
            for j in rotations.keys():
                if done:
                    break
                for k in rotations.keys():
                    if counter > var - 1:
                        done = True
                        break
                    else:
                        rotations[k]()
                        rotations[j]()
                        rotations[i]()
                        counter += 1



class Box(AbstractBox):
    def __init__(self, size, mass, fragile, is_rotatebleXYZ):
        super().__init__(size, is_rotatebleXYZ)
        self.mass = mass
        self.fragile = fragile
        self.id = None


    def getattrs(self):
        output_dict = {}
        output_dict['size'] = self.size
        output_dict['position'] = [
                               self.position[0] + self.size[0] / 2,
                               self.position[1] + self.size[1] / 2,
                               self.position[2] + self.size[2] / 2
                               ]

        return [output_dict]

    def putOnPos(self, position):
        self.position = position



class Barrel(AbstractBox):
    def __init__(self, size, mass, fragile, is_rotatebleXYZ):
        super().__init__(size, is_rotatebleXYZ)
        self.mass = mass
        self.fragile = fragile

#
class Container:
    def __init__(self, size):
        self.size = size
        self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]

    def put(self, box, position):
        for i in range(position[2], position[2] + box.size[2]):  # Z
            for j in range(position[1], position[1] + box.size[1]):  # Y
                for k in range(position[0], position[0] + box.size[0]):  # X
                    self.space[k][j][i] = box.id

        box.putOnPos(position)

    def space_print(self):
        for i in range(self.size[2]):  # Z
            for j in range(self.size[1]):  # Y
                for k in range(self.size[0]):  # X
                    if self.space[k][j][i] == None:
                        print('N', end='\t')
                    else:
                        print(self.space[k][j][i], end='\t')
                print()
            print()


class Block(Container, AbstractBox):
    def __init__(self, size, is_rotatebleXYZ):
        AbstractBox.__init__(self, size=size, is_rotatableXYZ=is_rotatebleXYZ)
        Container.__init__(self, size=size)
        self.mass = 0
        self.boxes = []
        self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]

    def put(self, box, position):
        super().put(box, position)
        self.boxes.append(box)
        self.mass += box.mass

    def pop(self, box_id):
        for idx, key in self.boxes:
            if key == box_id:
                self.boxes.pop(idx)
                break

    def getattrs(self):
        output_list = []
        for box in self.boxes:
            output_list.append(box.getattrs()[0])

        return output_list

    def putOnPos(self, position):
        self.position = position

        for box in self.boxes:
            box.position = [i+j for i,j in zip(box.position, self.position)]


    def load_identity(self):
        pass

    def rotateX(self):
        AbstractBox.rotateX(self)
        for box in self.boxes:
            box.rotateX()
            box.putOnPos((Rx.dot(box.position)).tolist())


    def rotateY(self):
        AbstractBox.rotateY(self)
        for box in self.boxes:
            box.rotateY()
            box.putOnPos((Ry.dot(box.position)).tolist())

    def rotateZ(self):
        AbstractBox.rotateZ(self)
        for box in self.boxes:
            box.rotateZ()
            box.putOnPos((Rz.dot(box.position)).tolist())





