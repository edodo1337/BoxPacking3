#pragma once
#include <array>
#include <vector>
#include <iostream>
#include <iterator>
#include <algorithm>
// #include <boost/lambda/lambda.hpp>
// #include <boost/numeric/ublas/vector.hpp>
// #include <boost/numeric/ublas/matrix.hpp>
// #include <boost/numeric/ublas/io.hpp>
// #include <boost/numeric/ublas/assignment.hpp>
// using namespace boost::numeric::ublas;

class AbstractBox
{
    private:
        std::array<int,3> position;
        std::array<int,3> diag;
        std::array<int,3> size;
        int id;
        int rotation_sate;
        int rotation_variants;
        bool is_rotatableX;
        bool is_rotatableY;
        bool is_rotatableZ;
        
    
    public:
        static int boxes_count;
        std::array<int,3> get_position();
        std::array<int,3> get_diag();
        std::array<int,3> get_size();
        int get_id();
        void set_position(std::array<int,3> &position);
        void set_diag(std::array<int,3> &diag);
        void set_size(std::array<int,3> &diag);
        void putOnPos(std::array<int,3> &pos);
        void rotateX();
        void rotateY();
        void rotateZ();
        void rotateXi();    //inverse rotations
        void rotateYi();
        void rotateZi();
        AbstractBox();
        AbstractBox(std::array<int,3> &size, std::array<bool,3> &is_rotatableXYZ);
};
