from utils import Rx, Ry, Rz, Qx, Qy, Qz
import numpy as np


class AbstractCargoBay:
    counter = 0

    #   абстрактный класс контейнера
    def __init__(self, **params):
        self.size = params['size']
        self.id = self.__set_id__()
        self.placed_items = set()
        self.points = set()
        self.points.add((0, 0, 0))
        self.carrying_capacity = params.get('carrying_capacity', 10000000000)

    @staticmethod
    def __set_id__():
        AbstractCargoBay.counter += 1
        return AbstractCargoBay.counter

    def put(self, box, position):
        box.putOnPos(position)
        _box = Box()
        _box.copy_attrs(box)
        self.placed_items.add(_box)
        self.points.add((box.position[0] + box.diag[0], box.position[1], box.position[2]))
        self.points.add((box.position[0], box.position[1] + box.diag[1], box.position[2]))
        self.points.add((box.position[0] + box.diag[0], box.position[1] + box.diag[1], box.position[2] + box.diag[2]))
        self.points.add((box.position[0] + box.diag[0], box.position[1], box.position[2] + box.diag[2]))
        self.points.add((box.position[0], box.position[1] + box.diag[1], box.position[2] + box.diag[2]))
        self.points.add((box.position[0] + box.diag[0], box.position[1] + box.diag[1], box.position[2] + box.diag[2]))
        self.points.add((box.position[0], box.position[1], box.position[2] + box.diag[2]))
        for point in self.points:
            if (point[0] > self.size[0] or point[0] < 0) or (point[1] > self.size[1] or point[1] < 0) \
                    or (point[2] > self.size[2] or point[0] < 0):
                del point

class ISOContainer(AbstractCargoBay):
    pass


class AbstractBox:  # абстрактный класс коробки
    counter = 0

    def __init__(self, **params):
        self.id = self.__set_id__()
        self.size = params.get('size', None)
        self.default_size = self.size[:] if self.size else None
        self.diag = np.asarray([self.size[0], self.size[1], self.size[2]]) if self.size else None
        self.position = None
        self.relative_position = None
        self.is_rotatableX = params.get('is_rotatableX', True)
        self.is_rotatableY = params.get('is_rotatableY', True)
        self.is_rotatableZ = params.get('is_rotatableZ', True)
        self.rotation_state = 0
        self.rotation_variants = 9
        self.fragile = params.get('fragile', False)
        self.mass = params.get('mass', 0)
        self.color = params.get('color', '#bbbbbb')

    # def __init__(self, size, is_rotatableXYZ, is_fragile):
    #     self.size = size
    #     self.id = self.__set_id__()
    #     self.default_size = size[:]
    #     self.position = None
    #     self.relative_position = None
    #     self.diag = np.asarray([self.size[0], self.size[1], self.size[2]])
    #     self.is_rotatableX = is_rotatableXYZ[0]
    #     self.is_rotatableY = is_rotatableXYZ[1]
    #     self.is_rotatableZ = is_rotatableXYZ[2]
    #     self.rotation_state = 0
    #     self.rotation_variants = 9
    #     self.fragile = is_fragile
    #     self.color = "#bbbbbb"

    @staticmethod
    def __set_id__():
        AbstractBox.counter += 1
        return AbstractBox.counter

    def load_identity(self):
        self.size = self.default_size[:]
        self.diag = [self.size[0], self.size[1], self.size[2]]
        # self.rotation_state = 0

    def rotateX(self):
        if self.is_rotatableX:
            self.size[1], self.size[2] = self.size[2], self.size[1]
            if self.position:
                self.position = Rx.dot(self.position)
            self.diag = Rx.dot(self.diag)

    def rotateY(self):
        if self.is_rotatableY:
            self.size[0], self.size[2] = self.size[2], self.size[0]
            if self.position:
                self.position = Ry.dot(self.position)
            self.diag = Ry.dot(self.diag)

    def rotateZ(self):
        if self.is_rotatableZ:
            self.size[0], self.size[1] = self.size[1], self.size[0]
            if self.position:
                self.position = Rz.dot(self.position)
            self.diag = Rz.dot(self.diag)

    #       вращения в обратную сторону (используется в данный момент, т.к. они работают лучше, не знаю почему)
    def rotateXi(self):
        if self.is_rotatableX:
            self.size[1], self.size[2] = self.size[2], self.size[1]
            if self.position:
                self.position = Qx.dot(self.position)
            self.diag = Qx.dot(self.diag)

    def rotateYi(self):
        if self.is_rotatableY:
            self.size[0], self.size[2] = self.size[2], self.size[0]
            if self.position:
                self.position = Qy.dot(self.position)
            self.diag = Qy.dot(self.diag)

    def rotateZi(self):
        if self.is_rotatableZ:
            self.size[0], self.size[1] = self.size[1], self.size[0]
            if self.position:
                self.position = Qz.dot(self.position)
            self.diag = Qz.dot(self.diag)

    def putOnPos(self, position):
        self.position = np.asarray(position)

    def tryRotations(self):
        self.rotation_state += 1
        a = lambda: None
        rotations = {
            '0': a,  # пустой метод, который ничего не делает
            '1': self.rotateXi,
            '2': self.rotateYi,
            '3': self.rotateZi,
            '4': self.rotateX,
            '5': self.rotateY,
            '6': self.rotateZ,
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
                    if counter > self.rotation_state:
                        done = True
                        break
                    else:
                        self.load_identity()
                        rotations[k]()
                        rotations[j]()
                        rotations[i]()

                        counter += 1

    def copy_attrs(self, box):
        self.id = box.id
        self.size = box.size
        self.default_size = box.default_size
        self.diag = box.diag
        self.position = box.position
        self.relative_position = box.relative_position
        self.rotation_variants = box.rotation_variants
        self.rotation_state = box.rotation_state
        self.fragile = box.fragile
        self.mass = box.mass
        self.color = box.color

    def __str__(self):
        return f"<Box: id:{self.id} size:{self.size} pos:{self.position}>"


class Box(AbstractBox):
    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, position):
        self.__position = position

    @property
    def diag(self):
        return self.__diag

    @diag.setter
    def diag(self, diag):
        self.__diag = diag

    def copy_attrs(self, box):
        super().copy_attrs(box)
