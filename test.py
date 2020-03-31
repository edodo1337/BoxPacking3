from entities import *
from copy import deepcopy
from algorithms import *
from utils import *
from entities import *
from drawing import *
import ctypes


@profile
def test():
    boxes = [Box(size=[8, 4, 2]) for i in range(55)]
    cont = ISOContainer(size=[25, 25, 25])
    for box in boxes:
        find_place(box, cont)
    draw(cont.size[0], cont.size[1], cont.size[2], boxes)



test()
profile.print_stats()

# pos1 = [0,0,0]
# diag1 = [5,5,5]
#
#
# pos2 = [4,4,4]
# diag2 = [5,5,5]

# print(liblibgls_check_boxes_intersect(pos1, diag1, pos2, diag2).contents[:])
