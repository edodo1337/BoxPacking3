import numpy as np
from copy import copy
from utils import Rx, Ry, Rz, Qx, Qy, Qz
from settings import global_box_counter



class BoxDatabase():
    def __init__(self):
        self.items = dict()

    def add(self, *args):
        for item in args:
            self.items[str(item.id)] = item


    def get(self, id):
        return self.items.get(str(id))

    def remove(self, id):
        box = self.get(str(id))
        del box
        del self.items[str(id)]


class AbstractContainer:
    def __init__(self, size):
        self.size = size
        self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]
        self.items = {}

    def put(self, box, position):
        for i in range(position[2], position[2] + box.size[2]):  # Z
            for j in range(position[1], position[1] + box.size[1]):  # Y
                for k in range(position[0], position[0] + box.size[0]):  # X
                    self.space[k][j][i] = box.id
        box.putOnPos(position)
        self.items[str(box.id)] = box

    def pop(self, box):
        for i in range(box.position[2], box.position[2] + box.size[2]):  # Z
            for j in range(box.position[1], box.position[1] + box.size[1]):  # Y
                for k in range(box.position[0], box.position[0] + box.size[0]):  # X
                    self.space[k][j][i] = None

        del self.items[str(box.id)]

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



class AbstractBox:
    def __init__(self, size, is_rotatableXYZ):
        self.size = size
        global global_box_counter
        global_box_counter += 1
        self.id = global_box_counter - 1
        #print('ID', self.id)
        self.default_size = size[:]
        self.position = None
        self.diag = [self.size[0], self.size[1], self.size[2]]
        self.is_rotatableX = is_rotatableXYZ[0]
        self.is_rotatableY = is_rotatableXYZ[1]
        self.is_rotatableZ = is_rotatableXYZ[2]

    @staticmethod
    def get_count():
        global global_box_counter
        return global_box_counter

    def load_identity(self):
        self.size = self.default_size[:]
        self.diag = [1,1,1]

    def rotateX(self):
        self.size[1], self.size[2] = self.size[2], self.size[1]
        self.diag = (Rx.dot(self.diag)).tolist()

    def rotateY(self):
        self.size[0], self.size[2] = self.size[2], self.size[0]
        self.diag = (Ry.dot(self.diag)).tolist()

    def rotateZ(self):
        self.size[0], self.size[1] = self.size[1], self.size[0]
        self.diag = (Rz.dot(self.diag)).tolist()

    def rotateX(self):
        self.size[1], self.size[2] = self.size[2], self.size[1]
        self.diag = (Qx.dot(self.diag)).tolist()

    def rotateY(self):
        self.size[0], self.size[2] = self.size[2], self.size[0]
        self.diag = (Qy.dot(self.diag)).tolist()

    def rotateZ(self):
        self.size[0], self.size[1] = self.size[1], self.size[0]
        self.diag = (Qz.dot(self.diag)).tolist()



    def tryRotations(self, var):
        a = lambda: None
        rotations = {
            '0': a,
            '1': self.rotateX,
            '2': self.rotateY,
            '3': self.rotateZ,
            '4': self.rotateXi,
            '5': self.rotateYi,
            '6': self.rotateZi
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


    def getattrs(self):
        output_dict = {}
        output_dict['position'] = [
            self.position[0],
            self.position[1],
            self.position[2],
        ]

        output_dict['diag'] = [
            self.diag[0],
            self.diag[1],
            self.diag[2]
        ]

        return [output_dict]

    def putOnPos(self, position):
        self.position = position



class Container(AbstractContainer):
    pass



class Block(AbstractContainer, AbstractBox):
    def __init__(self, size, is_rotatebleXYZ):
        AbstractBox.__init__(self, size=size, is_rotatableXYZ=is_rotatebleXYZ)
        AbstractContainer.__init__(self, size=size)
        self.mass = 0
        self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]

    def put(self, box, position):
        super().put(box, position)
        #self.items.append(box)
        self.mass += box.mass

    # def pop(self, box_id):
    #     for idx, key in self.items:
    #         if key == box_id:
    #             self.items.pop(idx)
    #             break

    def getattrs(self):
        output_list = []
        for box in self.items.values():
            output_list.append(box.getattrs()[0])
        return output_list

    def putOnPos(self, position):
        self.position = position
        for box in self.items.values():
            box.position = [i+j for i,j in zip(box.position, self.position)]


    def load_identity(self):
        pass

    def rotateX(self):
        temp = self.position[:]
        for box in self.items.values():
            self.putOnPos([self.size[0]/2, self.size[1]/2, self.size[2]/2])
            AbstractBox.rotateX(self)
            box.rotateX()
        self.position = temp

    def rotateY(self):
        AbstractBox.rotateY(self)
        self.putOnPos([-self.size[0] / 2, -self.size[1] / 2, -self.size[2] / 2])
        for box in self.items.values():
            box.putOnPos((Ry.dot(box.position)).tolist())
            box.rotateY()
        #self.position = (Ry.dot(self.position)).tolist()
        self.putOnPos([self.size[0]/2, self.size[1]/2, self.size[2]/2])

    def rotateZ(self):
        AbstractBox.rotateZ(self)
        self.putOnPos([-self.size[0] / 2, -self.size[1] / 2, -self.size[2] / 2])
        for box in self.items.values():
            box.putOnPos((Rz.dot(box.position)).tolist())
            box.rotateZ()
        # self.position = (Ry.dot(self.position)).tolist()
        self.putOnPos([self.size[0] / 2, self.size[1] / 2, self.size[2] / 2])





