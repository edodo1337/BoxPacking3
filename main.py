from entities import *
from drawing import *
import json


#mode = int(input("Mode: "))

mode = 0
boxes = []

if mode==0:
    cont = Container([5,5,5])
    N = 25
    max_size = 3

    for i in range(N):
        fragile = (np.random.choice(range(10), 1)) % 4 == 0
        #fragile = True
        # print(fragile)
        size = np.random.choice(range(1, max_size), 3)
        if (not fragile):
            if (size[0] < size[2]):
                size[0], size[2] = size[2], size[0]
            if (size[1] < size[2]):
                size[1], size[2] = size[2], size[1]
        else:
            if (size[0] > size[2]):
                size[0], size[2] = size[2], size[0]
            if (size[1] > size[2]):
                size[1], size[2] = size[2], size[1]

        boxes.append(Box(size, fragile))

elif mode == 1:
    f = open("input.json", "r").read()
    f_json = json.loads(f)
    boxes_json = []
    cont = None

    for i in f_json:
        if i['type'] == "container":
            cont = Container(i['size'])
        if i['type'] == "box":
            boxes_json.append(i)

    for box in boxes_json:
        size = box['size']
        if not box['fragile']:
            if (size[0] < size[2]):
                size[0], size[2] = size[2], size[0]
            if (size[1] < size[2]):
                size[1], size[2] = size[2], size[1]
        else:
            if (size[0] > size[2]):
                size[0], size[2] = size[2], size[0]
            if (size[1] > size[2]):
                size[1], size[2] = size[2], size[1]
        print(size, box['fragile'])
        boxes.append(Box(size, box['fragile']))



boxes.sort(key=lambda x: x.size[0]*x.size[1]*x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0]*x.size[1], reverse=True)
boxes.sort(key=lambda x: x.fragile == True, reverse=False)


for box in boxes:
    cont.put(box)

#cont.space_print()




fig = plt.figure()
ax = fig.gca(projection='3d')

pc = plotCubeAt(positions, sizes, colors=colors, edgecolor="k")
ax.add_collection3d(pc)

ax.set_xlim([0, cont.l])
ax.set_ylim([0, cont.w])
ax.set_zlim([0, cont.h])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()