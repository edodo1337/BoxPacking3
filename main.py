from entities import *
from utils import *
import json


boxdb = BoxDatabase()

def read_data(filename):
    f = open(filename, "r").read()
    f_json = json.loads(f)

    for item in f_json:
        size = item['size']
        mass = item['mass']
        fragile = item['fragile']
        is_rotatableXYZ = item['is_rotatableXYZ']

        boxdb.put(Box(size, mass, fragile, is_rotatableXYZ))




box1 = Box([1, 1, 1], 5, True, [True, True, True])
box1.position = [2, 2, 2]
box2 = Box([1, 1, 1], 5, True, [True, True, True])
box2.position = [3,3,3]
box3 = Box([1, 1, 1], 5, True, [True, True, True])

block = Block([3, 3, 3], [True, True, True])

boxdb.put(box1, box2)
#
# cont = Container([7, 7, 7])
#
#
# boxdb.box_list.sort(key=lambda x: obj3D_functional(x), reverse=True)
# boxdb.box_list.sort(key=lambda x: obj2D_functional(x), reverse=True)
#
# # print(block.id)
# # block.put(box1, [0, 0, 0])
# # block.put(box2, [1, 0, 0])
# # block.put(box2, [2, 0, 0])
# # cont.put(block, [0, 0, 0])
# # cont.space_print()
# # print(boxdb.get(1).size)
#
# for item in boxdb.box_list:
#     pos = find_place(cont, item)
#     print(pos)
#     if pos!=None:
#         cont.put(item, pos)
#
#cont.space_print()

write_positions(boxdb, "output.json")