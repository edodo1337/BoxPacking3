#pragma once

#include <iostream>
#include <iterator>
#include <algorithm>
#include <array>
// #include <boost/lambda/lambda.hpp>
// #include <boost/numeric/ublas/vector.hpp>
// #include <boost/numeric/ublas/matrix.hpp>
// #include <boost/numeric/ublas/io.hpp>
#include <time.h>
// #include <boost/numeric/ublas/assignment.hpp>


bool check_rects_intersect(std::array<int,2> &pos1, std::array<int,2> &diag1, 
                        std::array<int,2> &pos2, std::array<int,2> &diag2);
bool dot_inside_rect(float *pos1, float *pos2, float *diag2);
bool check_lines_intersect(std::array<int,2> &line1, std::array<int,2> &line2);
bool check_line_face_intersect(int line[2][2], int face[2][2]);


// std::array< std::array<int,3>, 3> Ry;
// std::array< std::array<int,3>, 3> Rz;
// std::array< std::array<int,3>, 3> Qx;
// std::array< std::array<int,3>, 3> Qy;
// std::array< std::array<int,3>, 3> Qz;



std::array<int,3> prod(std::array<std::array<int,3>,3> &matrix, std::array<int,3> &vector);
std::array<std::array<int,3>,3> prod(std::array<std::array<int,3>,3> matrix1, std::array<std::array<int,3>,3> matrix2);

std::array<int,3> prod(const std::array<const std::array<int,3>,3> &matrix, std::array<int,3> &vector);
std::array<std::array<int,3>,3> prod(const std::array<const std::array<int,3>,3> matrix1, std::array<std::array<int,3>,3> matrix2);




// using namespace boost::numeric::ublas;


// const auto Rx = [](){
//         matrix<int> m(3,3);
//         m <<= 1, 0, 0, 0, 0, -1, 0, 1, 0;
//         return m;
//         }();

// const auto Ry = [](){
//         matrix<int> m(3,3);
//         m <<= 0, 0, 1, 0, 1, 0, -1, 0, 0;
//         return m;
//         }();

// const auto Rz = [](){
//         matrix<int> m(3,3);
//         m <<= 0, -1, 0, 1, 0, 0, 0, 0, 1;
//         return m;
//         }();


// const auto Qx = [](){
//         matrix<int> m(3,3);
//         m <<= 1, 0, 0, 0, 0, 1, 0, -1, 0;
//         return m;
//         }();

// const auto Qy = [](){
//         matrix<int> m(3,3);
//         m <<= 0, 0, -1, 0, 1, 0, 1, 0, 0;
//         return m;
//         }();

// const auto Qz = [](){
//         matrix<int> m(3,3);
//         m <<= 0, 1, 0, -1, 0, 0, 0, 0, 1;
//         return m;
//         }();

const std::array< const std::array<int,3>, 3> Rx = {{
    {1,0,0},
    {0,0,-1},
    {0,1,0}
}};


const std::array< const std::array<int,3>, 3> Ry = {{
    {0,0,1},
    {0,1,0},
    {-1,0,0}
}};


const std::array< const std::array<int,3>, 3> Rz = {{
    {0,-1,0},
    {1,0,0},
    {0,0,1}
}};


const std::array< const std::array<int,3>, 3> Qx = {{
    {1,0,0},
    {0,0,1},
    {0,-1,0}
}};


const std::array< const std::array<int,3>, 3> Qy = {{
    {0,0,-1},
    {0,1,0},
    {1,0,0}
}};


const std::array< const std::array<int,3>, 3> Qz = {{
    {0,1,0},
    {-1,0,0},
    {0,0,1}
}};
