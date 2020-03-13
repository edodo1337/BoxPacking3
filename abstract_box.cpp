#include <iostream>
#include <array>
#include "abstract_box.h"

int AbstractBox::boxes_count = 0;

std::array<int,3> AbstractBox::get_position()
    {   
        return this->position;
    }   

std::array<int,3> AbstractBox::get_diag()
    {   
        return this->diag;
    }   

int AbstractBox::get_id()
    {   
        return this->id;
    } 

void AbstractBox::set_position(std::array<int,3> &position)
    {   
        for (int i(0); i<3; i++)
        {
            this->position.at(i) = position.at(i);
        }
    } 

void AbstractBox::set_diag(std::array<int,3> &diag)
    {   
        for (int i(0); i<3; i++)
        {
            this->diag.at(i) = diag.at(i);
        }
    } 

void AbstractBox::putOnPos(std::array<int,3> &pos)
{
    this->set_position(pos);
}

AbstractBox::AbstractBox(std::array<int,3> &diag, std::array<bool,3> &is_rotatableXYZ)
    {
        this->set_diag(diag);
        this->is_rotatableX = is_rotatableXYZ.at(0);
        this->is_rotatableY = is_rotatableXYZ.at(1);
        this->is_rotatableZ = is_rotatableXYZ.at(2);
        this->rotation_sate = 0;
        this->id = ++this->boxes_count;
    }

AbstractBox::AbstractBox()
    {
        this->id = ++this->boxes_count;
    }


// int main()
// {   
//     std::array<int,3> pos = {5,2,3};
//     std::array<int,3> diag = {5,5,5};
//     std::array<bool,3> is_rotatableXYZ = {true, true, true};
    
//     AbstractBox box1(pos, diag, is_rotatableXYZ);
//     AbstractBox box2(pos, diag, is_rotatableXYZ);



//     return 0;
// }