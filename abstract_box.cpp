#include <iostream>
#include <array>
#include <vector>
#include "abstract_box.h"
#include "utils.h"
#include <iterator>
#include <algorithm>
// #include <boost/lambda/lambda.hpp>
// #include <boost/numeric/ublas/vector.hpp>
// #include <boost/numeric/ublas/matrix.hpp>
// #include <boost/numeric/ublas/io.hpp>
// #include <boost/numeric/ublas/assignment.hpp>
#include <time.h>
// using namespace boost::numeric::ublas;


int AbstractBox::boxes_count = 0;

std::array<int,3> AbstractBox::get_position()
    {   
        return this->position;
    }   

std::array<int,3> AbstractBox::get_diag()
    {   
        return this->diag;
    }   

std::array<int,3> AbstractBox::get_size()
    {   
        return this->size;
    }   

int AbstractBox::get_id()
    {   
        return this->id;
    } 

void AbstractBox::set_position(std::array<int,3> &position)
    {   
        this->position = position;
    } 

void AbstractBox::set_diag(std::array<int,3> &diag)
    {   
        this->diag = diag;
    } 

void AbstractBox::set_size(std::array<int,3> &size)
    {   
        this->size = size;
    } 

void AbstractBox::putOnPos(std::array<int,3> &pos)
{
    this->set_position(pos);
}

AbstractBox::AbstractBox(std::array<int,3> &size, std::array<bool,3> &is_rotatableXYZ)
    {
        this->size = size;
        this->diag = {0,0,0};
        this->is_rotatableX = is_rotatableXYZ.at(0);
        this->is_rotatableY = is_rotatableXYZ.at(1);
        this->is_rotatableZ = is_rotatableXYZ.at(2);
        this->rotation_sate = 0;
        this->id = ++this->boxes_count;
    }


void AbstractBox::rotateX()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Rx, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[0], s[2], s[1]};
    }

void AbstractBox::rotateY()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Ry, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[2], s[1], s[0]};
    }

void AbstractBox::rotateZ()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Rz, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[1], s[0], s[2]};
    }

void AbstractBox::rotateXi()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Qx, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[0], s[2], s[1]};
    }

void AbstractBox::rotateYi()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Qy, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[2], s[1], s[0]};
    }

void AbstractBox::rotateZi()
    {
        auto d = this->get_diag();
        std::array<int,3> diag = prod(Qz, d);
        this->diag = diag;
        auto s = this->size;
        this->size = {s[1], s[0], s[2]};
    }

AbstractBox::AbstractBox()
    {
        this->id = ++this->boxes_count;
    }

    



// int main()
// {   

//     std::array<int,3> diag{1,2,3};
//     std::array<bool,3> is_rotatableXYZ{true, true, true};
//     std::array<int,3> pos{5,5,5};

//     auto box = AbstractBox(diag, is_rotatableXYZ);
    
//     box.rotateY();
//     box.set_position(pos);

//     for (auto i:box.get_diag())
//         std::cout<<i<< " ";
        

//     return 0;
// }