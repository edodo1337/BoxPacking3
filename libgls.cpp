#include <stdbool.h>
#include <stdio.h>
#include "libgls.h"
#include <iostream>

extern "C" bool check_rectangles_intersect(int *pos1, int *diag1, int *pos2, int *diag2)
{
    if ((pos1[0] <= pos2[0]) && (pos2[0]<diag1[0]) || 
        (pos1[0] < diag2[0]) && (diag2[0]<=diag1[0]) || 
        (pos2[0] <= pos1[0]) && (pos1[0]<diag2[0]) ||
        (pos2[0] < diag1[0]) && (diag1[0]<=diag2[0]))
    {
        if ((pos1[1] <= pos2[1]) && (pos2[1]<diag1[1]) || 
            (pos1[1] < diag2[1]) && (diag2[1]<=diag1[1]) || 
            (pos2[1] <= pos1[1]) && (pos1[1]<diag2[1]) ||
            (pos2[1] < diag1[1]) && (diag1[1]<=diag2[1]))
        {
            return false;
        }
    }
    return true;
}

bool check_1d_lines_intersect(int (&line1)[2], int (&line2)[2])
{
    if ((line1[0] < line2[0] && line2[1] < line1[1] || line1[0] < line2[1] && line1[1]) ||
        (line2[0] < line1[0] && line1[1] < line2[1] || line2[0] < line1[1] && line2[1]))
        {
            return true;
        }
    else
        return false;
}


extern "C" bool check_dot_in_rectangle(float *pos1, float *pos2, float *diag2)
{
    if ((pos2[0] < pos1[0]) && (pos1[0] < diag2[0]))
    {
        if ((pos2[1] < pos1[1]) && (pos1[1] < diag2[1]))
        {
            return true;
        }
    }
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

int main()
{
    int line1[2] = {0,5};
    int line2[2] = {5,7};
    bool b = check_1d_lines_intersect(line1, line2);
    std::cout << b << std::endl;
    return 0;
}