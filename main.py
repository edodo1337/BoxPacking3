from algorithms import *
from utils import *
from entities import *
from drawing import *

boxes = [Box(size=[2,2,2]) for i in range(25)]

cont = ISOContainer(size=[10, 10, 10])

for box in boxes:
    find_place(box, cont)


draw(10, 10, 10, boxes)
