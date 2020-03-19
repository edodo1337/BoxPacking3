#pragma once
#include <stdbool.h>
#include "abstract_box.h"

#ifdef  __cplusplus
extern "C" {
#endif
    bool check_rectangles_intersect(int (&pos1)[2], int (&diag1)[2], int (&pos2)[2], int (&diag2)[2]);
    bool check_dot_in_rectangle(float (&pos1)[2], float (&pos2)[2], float (&diag2)[2]);
    bool check_1d_lines_intersect(int (&line1)[2], int (&line2)[2]);
}

std::array<bool,3>* check_boxes_intersect(AbstractBox box1, AbstractBox box2);