import ctypes as c
from ctypes import pointer
import line_profiler

profile = line_profiler.LineProfiler()
#ctypes.POINTER(ctypes.c_int)
_libgls_check_boxes_intersect = c.CDLL('./libgls.so')
_libgls_check_boxes_intersect.check_boxes_intersect.restype = c.POINTER(c.c_bool*3)
# _libgls_check_boxes_intersect.check_boxes_intersect.restype = c.c_int32
_libgls_check_boxes_intersect.check_boxes_intersect.argtypes = [(c.c_int32*3), (c.c_int32*3), (c.c_int32*3), (c.c_int32*3)]



def liblibgls_check_boxes_intersect(pos1, diag1, pos2, diag2):
    def list_to_ar(arr):
        res = (c.c_int * len(arr))(*arr)
        return res
    _p1 = list_to_ar(pos1)
    _d1 = list_to_ar(diag1)
    _p2 = list_to_ar(pos2)
    _d2 = list_to_ar(diag2)

    return _libgls_check_boxes_intersect.check_boxes_intersect(_p1, _d1, _p2, _d2)




def is_fit(box, position, cargo_bay):
    if not((0 <= box.diag[0] + position[0] <= cargo_bay.size[0]) and
           (0 <= box.diag[1] + position[1] <= cargo_bay.size[1]) and
            (0 <= box.diag[2] + position[2] <= cargo_bay.size[2])):
        return [False]

    for item in cargo_bay.placed_items:
        # checkXYZ = check_boxes_intersect(item.position, item.diag, position, box.diag)
        checkXYZ = liblibgls_check_boxes_intersect(item.position, item.diag, position, box.diag).contents[:]

        if checkXYZ[0] and checkXYZ[1] and checkXYZ[2]:
            return [False]

    return [True]


def find_place(box, cargo_bay):
    points = list(cargo_bay.points)
    points.sort(key = lambda x: x[2])
    for point in points:
        if is_fit(box, point, cargo_bay)[0]:
            cargo_bay.put(box,point)
            break




def check_boxes_intersect(pos1, diag1, pos2, diag2):
    line1_x = [min(pos1[0], pos1[0] + diag1[0]),
               max(pos1[0], pos1[0] + diag1[0])]
    line1_y = [min(pos1[1], pos1[1] + diag1[1]),
               max(pos1[1], pos1[1] + diag1[1])]
    line1_z = [min(pos1[2], pos1[2] + diag1[2]),
               max(pos1[2], pos1[2] + diag1[2])]

    line2_x = [min(pos2[0], pos2[0] + diag2[0]),
               max(pos2[0], pos2[0] + diag2[0])]
    line2_y = [min(pos2[1], pos2[1] + diag2[1]),
               max(pos2[1], pos2[1] + diag2[1])]
    line2_z = [min(pos2[2], pos2[2] + diag2[2]),
               max(pos2[2], pos2[2] + diag2[2])]

    check_x = line1_x[0] < line2_x[1] and line1_x[1] > line2_x[0]
    check_y = line1_y[0] < line2_y[1] and line1_y[1] > line2_y[0]
    check_z = line1_z[0] < line2_z[1] and line1_z[1] > line2_z[0]
    return [check_x, check_y, check_z]


def check_rects_intersect(pos1, diag1, pos2, diag2):
    line1x = [pos1[0], pos1[0] + diag1[0]]
    if line1x[0] > line1x[1]:
        line1x = [line1x[1], line1x[0]]

    line2x = [pos2[0], pos2[0] + diag2[0]]
    if line2x[0] > line2x[1]:
        line2x = [line2x[1], line2x[0]]

    line1y = [pos1[1], pos1[1] + diag1[1]]
    if line1y[0] > line1y[1]:
        line1y = [line1y[1], line1y[0]]

    line2y = [pos2[1], pos2[1] + diag2[1]]
    if line2y[0] > line2y[1]:
        line2y = [line2y[1], line2y[0]]

    return check_1d_lines_intersect(line1x, line2x), check_1d_lines_intersect(line1y, line2y)


def check_1d_lines_intersect(line1, line2):
    if line1[0] < line2[0] < line1[1] or line1[0] < line2[1] < line1[1] or \
            line2[0] < line1[0] < line2[1] or line2[0] < line1[1] < line2[1] or \
            (line1[0] == line2[0]) and (line1[1] == line2[1]):
        return True
    else:
        return False


