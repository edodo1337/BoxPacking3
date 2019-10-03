
COLOR = 1
count = 1

positions = []
sizes = []
colors = []

class Box:
    fragile = None
    position = None
    size = None
    color = None
    num = None
    default_size = None
    def __init__(self, size, fragile):
        global count
        self.size = size
        self.num = count
        self.fragile = fragile
        self.default_size = size
        count += 1

    def load_default_size(self):
        self.size = self.default_size

    def rotation(self, kind):
        if (kind == 0): #X
            self.load_default_size()
            self.size[1], self.size[0] = self.size[0], self.size[1]
        elif (kind == 1): #Y
            self.load_default_size()
            self.size[0], self.size[2] = self.size[2], self.size[0]
        elif (kind == 2): #Z
            self.load_default_size()
            self.size[1], self.size[2] = self.size[2], self.size[1]
        elif (kind == 3): #ZY
            self.load_default_size()
            self.rotation(2)
            self.rotation(1)
        elif (kind == 4): #ZX
            self.load_default_size()
            self.rotation(2)
            self.rotation(0)
        elif (kind == 5): #YX
            self.load_default_size()
            self.rotation(1)
            self.rotation(0)
        elif (kind == 6): #YZ
            self.load_default_size()
            self.rotation(1)
            self.rotation(2)
        elif (kind == 7): #XY
            self.load_default_size()
            self.rotation(0)
            self.rotation(1)
        elif (kind == 8): #XZ
            self.load_default_size()
            self.rotation(0)
            self.rotation(2)
        elif (kind == 9):
            self.load_default_size()
            self.rotation(0)
            self.rotation(2)
        elif (kind == 10):
            self.load_default_size()
            self.rotation(0)
            self.rotation(1)
            self.rotation(2)





class Container:
    def __init__(self, size):
        self.w = size[0]
        self.l = size[1]
        self.h = size[2]
        self.space = [[[0 for k in range(self.h)] for j in range(self.w)] for i in range(self.l)]


    def space_print(self):
        for i in range(self.h): #Z
            for j in range(self.w): #Y
                for k in range(self.l): #X
                    print(self.space[k][j][i], end='\t')
                print()
            print()

    def put(self, box):
        global positions
        global sizes
        global colors

        self.find(box)
        if (box.position!=None):
            for i in range(box.position[2], box.position[2]+box.size[2]): #Z
                for j in range(box.position[1], box.position[1]+box.size[1]): #Y
                    for k in range(box.position[0], box.position[0]+box.size[0]): #X
                        self.space[k][j][i] = box.color
            positions.append(box.position)
            sizes.append(box.size)
            if box.fragile:
                colors.append((0.5,0.5,0.5,0.5))
            else:
                colors.append("C0{}".format(box.color))
        else:
            print('No place', box.fragile)


    def find(self, box):
        global COLOR
        for i in range(self.h):
            for j in range(self.w):
                for k in range(self.l):
                    for ri in range(11):
                        box.rotation(ri)
                        if box.fragile:
                            if (box.size[0] > box.size[2]):
                                box.size[0], box.size[2] = box.size[2], box.size[0]
                            if (box.size[1] > box.size[2]):
                                box.size[1], box.size[2] = box.size[2], box.size[1]

                        if self.isFree([k, j, i], box):
                            box.position = [k, j, i]
                            if (box.fragile):
                                box.color = 0.5
                            else:
                                box.color = COLOR
                                COLOR += 1
                            #print('YES')
                            # print(box.position)
                            return
                        elif (j==self.w-1) and (k==self.l-1):
                            pass
                            #print(box.size, ri, [i,j,k])
                            #box.rotation(ri)


    def isFree(self, position, box):
        flag = True
        left_side = 0
        right_side = 0
        counter = 0
        try:
            for i in range(position[2], position[2] + box.size[2]):  # Z
                for j in range(position[1], position[1] + box.size[1]):  # Y
                    for k in range(position[0], position[0] + box.size[0]):  # X
                        if (position[2] > 0):
                            if (self.space[k][j][i-1]!=0):
                                counter += 1
                                #print(k,j)
                                # if (j < (position[1] + box.size[1]) // 2 +1) and (k < (position[0] + box.size[0]) // 2 + 1 ):
                                #     left_side += 1
                                # else:
                                #     right_side += 1


                            if (self.space[k][j][position[2]-1] == 0.5) or (self.space[k][j][position[2]+1] == 0.5):
                                #print('FRAGILE')
                                return False
                        if self.space[k][j][i]!=0:
                            return False


            if (position[2]>0):
                print("Fragile", box.fragile, counter)
                if (counter < (box.size[0]*box.size[1]) // 2 + 1 ):
                    flag = False
                    print("Flag", flag, box.size)


            return True and flag
        except:
            return False

