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

inline std::array<bool,3>* check_boxes_intersect(AbstractBox box1, AbstractBox box2)
{   
    std::array<int,3> pos1 = box1.get_position();
    std::array<int,3> pos2 = box2.get_position();
    std::array<int,3> diag1 = box1.get_diag();
    std::array<int,3> diag2 = box2.get_diag();
    std::array<int,3> size1 = box1.get_size();
    std::array<int,3> size2 = box2.get_size();
    static std::array<bool,3> checkXYZ{false, false, false};

    for (int i(0); i<3; i++)
    {
        if (diag1[i] < 0)
            pos1[i] = diag1[i] + pos1[i];

        if (diag2[i] < 0)
            pos2[i] = diag2[i] + pos2[i];
    }

    //check the X axis
    if(std::abs(pos1[0] - pos2[0]) < (size1[0]))
    {
        checkXYZ[0] = true;
        //check the Y axis
        if(std::abs(pos1[1] - pos2[1]) < (size1[1]))
        {
            checkXYZ[1] = true;
            //check the Z axis
            if(std::abs(pos1[2] - pos2[2]) < (size1[2]))
            {
                checkXYZ[2] = true;
            }
        }
    }

    return &checkXYZ;
}
