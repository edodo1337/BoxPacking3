from entities import *
from drawing import *





cont = Container(5,5,7)

N = 15
max_size = 4
boxes = []

for i in range(N):
    size = np.random.choice(range(1,max_size),3)
    if (size[0] < size[2]):
        size[0], size[2] = size[2], size[0]
    if (size[1] < size[2]):
        size[1], size[2] = size[2], size[1]
    boxes.append(Box(size))


boxes.sort(key=lambda x: x.size[0]*x.size[1]*x.size[2], reverse=True)
boxes.sort(key=lambda x: x.size[0]*x.size[1], reverse=True)


for box in boxes:
    cont.put(box)

#cont.space_print()



# box1 = Box([4,5,4])
# cont.put(box1)
#
# box2 = Box([5,1,2])
# cont.put(box2)

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