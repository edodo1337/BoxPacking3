#include <stdbool.h>
#include <stdio.h>
#include "libgls.h"
#include <array>
#include <iostream>
#include <cmath>

extern "C" bool check_rectangles_intersect(int (&pos1)[2], int (&diag1)[2], int (&pos2)[2], int (&diag2)[2])
{   
    int line1_x[2]{pos1[0], pos1[0] + diag1[0]};
    int line2_x[2]{pos2[0], pos2[0] + diag2[0]};
    int line1_y[2]{pos1[1], pos1[1] + diag1[1]};
    int line2_y[2]{pos2[1], pos2[1] + diag2[1]};

    bool x_lines = check_1d_lines_intersect(line1_x, line2_x);
    bool y_lines = check_1d_lines_intersect(line1_y, line2_y);
    return x_lines && y_lines;
}

extern "C" bool check_1d_lines_intersect(int (&line1)[2], int (&line2)[2])
{   
    int b_line1[2]{line1[0], line1[1]};
    int b_line2[2]{line2[0], line2[1]};

    if (line1[0] > line1[1])
        {   
            std::cout << "ASD ";
            b_line1[0] = line1[1]; b_line1[1] = line1[0];
        }
    
    if (line2[0] > line2[1])
        {
            std::cout << "ASD ";
            b_line2[0] = line2[1]; b_line2[1] = line2[0];
        }
        
    if ((b_line1[0] < b_line2[0] && b_line2[0] < b_line1[1] || b_line1[0] < b_line2[1] && b_line2[1] < b_line1[1]) ||
        (b_line2[0] < b_line1[0] && b_line1[0] < b_line2[1] || b_line2[0] < b_line1[1] && b_line1[1] < b_line2[1]) ||
        (b_line1[0] == b_line2[0] && b_line1[1] == b_line2[1]))
        {
            return true;
        }
    return false;
}


extern "C" bool check_dot_in_rectangle(float (&pos1)[2], float (&pos2)[2], float (&diag2)[2])
{
    if ((pos2[0] < pos1[0] && pos1[0] < diag2[0]) || (pos2[1] < pos1[1] && pos1[1] < diag2[1]))
        return true;
    return false;
}

extern "C" bool check_line_face_intersect(int line[4], int face[4])
{
    int x1, x2, y1, y2;
    bool checkX, checkY = false;

    if (line[0] > face[0])
    {
        x1 = face[0]; x2 = face[2];
        y1 = line[0]; y2 = line[2];
    } else
    {
        x1 = line[0]; x2 = line[2];
        y1 = face[0]; y2 = face[2];
    }
    
    if ((x1 <= y1) && (y1 < x2) || (x1 < y2) && (y2 <= x2))
    {
        checkX = true;
    }

    if (line[1] > face[1])
    {
        x1 = face[1]; x2 = face[3];
        y1 = line[1]; y2 = line[3];
    } else
    {
        x1 = line[1]; x2 = line[3];
        y1 = face[1]; y2 = face[3];
    }
    
    if ((x1 <= y1) && (y1 < x2) || (x1 < y2) && (y2 <= x2))
    {
        checkY = true;
    }

    if (checkX && checkY)
    {
        return true;
    } else
    {
        return false;
    }
}

// std::array<bool,3>* check_boxes_intersect(AbstractBox box1, AbstractBox box2)
// {   
//     std::array<int,3> pos1 = box1.get_position();
//     std::array<int,3> pos2 = box2.get_position();
//     std::array<int,3> diag1 = box1.get_diag();
//     std::array<int,3> diag2 = box2.get_diag();
//     std::array<int,3> size1 = box1.get_size();
//     std::array<int,3> size2 = box2.get_size();
//     static std::array<bool,3> checkXYZ{false, false, false};

//     for (int i(0); i<3; i++)
//     {
//         if (diag1[i] < 0)
//             pos1[i] = diag1[i] + pos1[i];

//         if (diag2[i] < 0)
//             pos2[i] = diag2[i] + pos2[i];
//     }

//     //check the X axis
//     if(std::abs(pos1[0] - pos2[0]) < (size1[0]))
//     {
//         checkXYZ[0] = true;
//         //check the Y axis
//         if(std::abs(pos1[1] - pos2[1]) < (size1[1]))
//         {
//             checkXYZ[1] = true;
//             //check the Z axis
//             if(std::abs(pos1[2] - pos2[2]) < (size1[2]))
//             {
//                 checkXYZ[2] = true;
//             }
//         }
//     }

//     return &checkXYZ;
// }

// int main()
// {
//     std::array<int,3> pos1{4,4,4};
//     std::array<int,3> diag1{5,5,5};
//     std::array<int,3> size1{5,5,5};

//     std::array<int,3> pos2{5,5,5};
//     std::array<int,3> diag2{2,2,2};
//     std::array<int,3> size2{2,2,2};

//     std::array<bool,3> is_rotatableXYZ{true, true, true};
    
//     AbstractBox box1 = AbstractBox(size1, is_rotatableXYZ);
//     AbstractBox box2 = AbstractBox(size2, is_rotatableXYZ);

//     box1.putOnPos(pos1);
//     box2.putOnPos(pos2);

//     box1.set_diag(diag1);
//     box2.set_diag(diag2);

//     bool b = check_boxes_intersect(box1, box2);

//     std::cout << b << std::endl;
//     return 0;
// }