#include <array>
#include "utils.h"
#include <iostream>

bool check_rects_intersect(std::array<int,2> &pos1, std::array<int,2> &diag1, 
                        std::array<int,2> &pos2, std::array<int,2> &diag2)
{
    std::array<int,2> line1 = { pos1.at(0), pos1.at(0) + diag1.at(0)};
    std::array<int,2> line2 = { pos2.at(0), pos2.at(0) + diag2.at(0)};
    bool checkX = check_lines_intersect(line1, line2);
    line1 = { pos1.at(1), pos1.at(1) + diag1.at(1)};
    line2 = { pos2.at(1), pos2.at(1) + diag2.at(1)};
    bool checkY = check_lines_intersect(line1, line2);
    return checkX && checkY;
}


bool dot_inside_rect(std::array<int,2> &pos1, std::array<int,2> &pos2, std::array<int,2> &diag2)
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

bool check_lines_intersect(std::array<int,2> &line1, std::array<int,2> &line2)
{
    if (
        (line2[0] < line1[0] && line1[0] < line2[1]) ||
        (line1[0] < line2[0] && line2[0] < line1[1])
    )
    {
        return true;
    } else
    {
        return false;
    }
        
}


bool check_line_face_intersect(std::array<std::array<int,2>,2> &line, 
                        std::array<std::array<int,2>,2> &face)
{
    int x1, x2, y1, y2;
    bool checkX, checkY = false;

    if (line[0][0] > face[0][0])
    {
        x1 = face[0][0]; x2 = face[1][0];
        y1 = line[0][0]; y2 = line[1][0];
    } else
    {
        x1 = line[0][0]; x2 = line[1][0];
        y1 = face[0][0]; y2 = face[1][0];
    }
    
    if ((x1 <= y1) && (y1 < x2) || (x1 < y2) && (y2 <= x2))
    {
        checkX = true;
    }

    if (line[1] > face[1])
    {
        x1 = face[0][1]; x2 = face[1][1];
        y1 = line[0][1]; y2 = line[1][1];
    } else
    {
        x1 = line[0][1]; x2 = line[1][1];
        y1 = face[0][1]; y2 = face[1][1];
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


// int main()
// {
//     std::array<int,2> pos1 = {0,0};
//     std::array<int,2> pos2 = {3,3};
//     std::array<int,2> diag1 = {3,3};
//     std::array<int,2> diag2 = {5,5};
    
//     std::cout << check_rects_intersect(pos1, diag1, pos2, diag2) << std::endl;


//     return 0;
// }