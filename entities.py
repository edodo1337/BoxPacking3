import numpy as np
from copy import copy
from utils import Rx, Ry, Rz, Qx, Qy, Qz, Ident
from settings import global_box_counter
import math

class BoxDatabase():  # больше не используется
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
    #   абстрактный класс контейнера, свободное пространство задается 3-матрицей, если ячейка == None, то она свободна
    #   иначе равна id коробки

    def __init__(self, size):
        self.size = size
        # self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in
        #               range(self.size[0])]
        self.items = {}
        self.points = [[0,0,0]]

    #   метод, который помещает коробку в спейс контейнера
    def put(self, box, position):
        stepZ = -1 if (position[2] + box.diag[2]) == 0 else int(
            (position[2] + box.diag[2]) / abs(position[2] + box.diag[2]))
        stepY = -1 if (position[1] + box.diag[1]) == 0 else int(
            (position[1] + box.diag[1]) / abs(position[1] + box.diag[1]))
        stepX = -1 if (position[0] + box.diag[0]) == 0 else int(
            (position[0] + box.diag[0]) / abs(position[0] + box.diag[0]))


        # for i in range(position[2], position[2] + box.diag[2], stepZ):  # Z
        #     for j in range(position[1], position[1] + box.diag[1], stepY):  # Y
        #         for k in range(position[0], position[0] + box.diag[0], stepX):  # X
        #             self.space[k][j][i] = box.id
        box.putOnPos(position)
        self.items[str(box.id)] = box

    # def put2(self, box, position):
    #     self.points.remove(position)
    #     self.points.append()

    #   метод, который удаляет коробку из спейса контейнера (не используется)
    def pop(self, box):
        for i in range(box.position[2], box.position[2] + box.size[2]):  # Z
            for j in range(box.position[1], box.position[1] + box.size[1]):  # Y
                for k in range(box.position[0], box.position[0] + box.size[0]):  # X
                    self.space[k][j][i] = None
        del self.items[str(box.id)]

    #   метод для вывода спейса контейнера в консоль (послойно)
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


class AbstractBox:  # абстрактный класс коробки
    def __init__(self, size, is_rotatableXYZ):
        self.size = size
        global global_box_counter
        global_box_counter += 1
        self.id = global_box_counter - 1
        # print('ID', self.id)
        self.default_size = size[:]
        self.position = None
        self.relative_position = None
        self.diag = [self.size[0], self.size[1], self.size[2]]
        self.is_rotatableX = is_rotatableXYZ[0]
        self.is_rotatableY = is_rotatableXYZ[1]
        self.is_rotatableZ = is_rotatableXYZ[2]
        self.rotation_state = 0

    @staticmethod
    def get_count():
        global global_box_counter
        return global_box_counter

    ###     методы вращения коробки по осям

    def load_identity(self):  # начальная ориентация коробки (не используется)
        self.size = self.default_size[:]
        self.diag = [self.size[0], self.size[1], self.size[2]]
        #self.rotation_state = 0

    def rotateX(self):
        if self.is_rotatableX:  # если нет запрета на вращение по оси
            self.size[1], self.size[2] = self.size[2], self.size[1]
            if self.position:
                self.position = (Rx.dot(self.position)).tolist()
            self.diag = (Rx.dot(self.diag)).tolist()
            self.diag = [abs(i) for i in self.diag]  # значение по модулу, т.к. работаем в положительных осях

    def rotateY(self):
        if self.is_rotatableY:
            self.size[0], self.size[2] = self.size[2], self.size[0]
            if self.position:
                self.position = (Ry.dot(self.position)).tolist()
            self.diag = (Ry.dot(self.diag)).tolist()
            self.diag = [abs(i) for i in self.diag]

    def rotateZ(self):
        if self.is_rotatableZ:
            self.size[0], self.size[1] = self.size[1], self.size[0]
            if self.position:
                self.position = (Rz.dot(self.position)).tolist()
            self.diag = (Rz.dot(self.diag)).tolist()
            self.diag = [abs(i) for i in self.diag]

    #       вращения в обратную сторону (используется в данный момент, т.к. они работают лучше, не знаю почему)
    def rotateXi(self):
        self.size[1], self.size[2] = self.size[2], self.size[1]
        if self.position:
            self.position = (Qx.dot(self.position)).tolist()
        self.diag = (Qx.dot(self.diag)).tolist()
        self.diag = [abs(i) for i in self.diag]

    def rotateYi(self):
        self.size[0], self.size[2] = self.size[2], self.size[0]
        if self.position:
            self.position = (Qy.dot(self.position)).tolist()
        self.diag = (Qy.dot(self.diag)).tolist()
        self.diag = [abs(i) for i in self.diag]

    def rotateZi(self):
        self.size[0], self.size[1] = self.size[1], self.size[0]
        if self.position:
            self.position = (Qz.dot(self.position)).tolist()
        self.diag = (Qz.dot(self.diag)).tolist()
        self.diag = [abs(i) for i in self.diag]

    def putOnPos(self, position):
        self.position = position

    def tryRotations(self):
        #   перебор вращений, работает кое как
        #   перебирает все (вроде бы) комбинации вращений коробки
        #   как набор вращений по 3 осям
        #   комбинация вращений кодируется 3мя числами. Напр. [0 2 3] - вращение по Y, затем по Z
        #   метод получает на вход десятичное число (фактически порядковый номер комбинации)
        self.rotation_state += 1
        a = lambda: None
        rotations = {
            '0': a, # пустой метод, который ничего не делает
            '1': self.rotateXi,
            '2': self.rotateYi,
            '3': self.rotateZi,
            # '4': self.rotateX,
            # '5': self.rotateY,
            # '6': self.rotateZ,
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
                        if k=='3':
                            if self.is_rotatableZ:
                                rotations[k]()
                        if k=='2':
                            if self.is_rotatableY:
                                rotations[j]()
                        if k=='1':
                            if self.is_rotatableX:
                                rotations[i]()

                        counter += 1


class Box(AbstractBox):  # класс коробки (обычной)
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

    #       не используется
    def Translate(self, position):
        if position is not None:
            pos = np.array(position)
            pos.reshape((3, 1))
            Trans = np.concatenate((Ident, pos))
            self.position = (Trans.dot(self.position)).tolist()
        else:
            self.position = position


class Container(AbstractContainer):
    pass


class Block(AbstractContainer, AbstractBox):
    #       класс блока (набора коробок)
    #       пока не используется, много проблем
    #       проблема с вращением блока в целом (совместно с коробками, чтобы их относительные позиции сохранялись)

    def __init__(self, size, is_rotatebleXYZ):
        AbstractBox.__init__(self, size=size, is_rotatableXYZ=is_rotatebleXYZ)
        AbstractContainer.__init__(self, size=size)
        self.mass = 0
        self.space = [[[None for k in range(self.size[2])] for j in range(self.size[1])] for i in range(self.size[0])]


    def put(self, box, position):
        super().put(box, position)
        box.relative_position = position
        self.mass += box.mass

    def getattrs(self):
        #       метод для получения выходных данных json
        output_list = []
        for box in self.items.values():
            output_list.append(box.getattrs()[0])
        return output_list

    def putOnPos(self, position):
        #   поместить блок и коробки внутри в позицию (типа групповая операция)
        self.position = position
        for box in self.items.values():
            box.position = [i + j for i, j in zip(box.relative_position, self.position)]

    def load_identity(self):
        pass

    def rotateX(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])
        AbstractBox.rotateX(self)

        for box in self.items.values():
            box.putOnPos([a - b for a, b in zip(box.position, box.relative_position)])
            box.rotateX()
            box.putOnPos([a + b for a, b in zip(box.position, box.relative_position)])
        self.putOnPos(temp_pos)

    def rotateY(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])
        AbstractBox.rotateY(self)

        for box in self.items.values():
            box.putOnPos([a - b for a, b in zip(box.position, temp_pos)])
            box.rotateY()
            box.putOnPos([a + b for a, b in zip(box.position, temp_pos)])
        self.putOnPos(temp_pos)

    def rotateZZ(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])

        AbstractBox.rotateZ(self)

        for box in self.items.values():
            # box.putOnPos([b for a, b in zip(box.position, box.relative_position)])
            box.position = box.relative_position[:]
            box.rotateZ()

            # box.putOnPos([a + b for a, b in zip(self.position, box.relative_position)])
            # box.putOnPos(self.position)

        self.putOnPos(temp_pos)

    def rotateXi(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])
        AbstractBox.rotateXi(self)

        for box in self.items.values():
            box.putOnPos([a - b for a, b in zip(box.position, temp_pos)])
            box.rotateXi()
            box.putOnPos([a + b for a, b in zip(box.position, temp_pos)])
        self.putOnPos(temp_pos)

    def rotateYi(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])
        AbstractBox.rotateYi(self)

        for box in self.items.values():
            box.putOnPos([a - b for a, b in zip(box.position, temp_pos)])
            box.rotateYi()
            box.putOnPos([a + b for a, b in zip(box.position, temp_pos)])
        self.putOnPos(temp_pos)

    def rotateZ(self):
        temp_pos = None
        if self.position:
            temp_pos = self.position[:]

        self.putOnPos([0, 0, 0])
        AbstractBox.rotateZi(self)

        for box in self.items.values():
            box.putOnPos([a - b for a, b in zip(box.position, temp_pos)])
            box.rotateZi()
            box.putOnPos([a + b for a, b in zip(box.position, temp_pos)])
        self.putOnPos(temp_pos)
