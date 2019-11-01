#BOX_COUNTER = 0


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


class Box(AbstractBox):
    def __init__(self, size, mass, fragile, is_rotatebleXYZ):
        super().__init__(size, is_rotatebleXYZ)
        self.mass = mass
        self.fragile = fragile

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
        #box.position = position

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

