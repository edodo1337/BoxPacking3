#include <iostream>
#include "abstract_container.h"


void AbstractContainer::set_size(std::array<int,3> &size)
    {
        this->size = size;
    }

void AbstractContainer::put(AbstractBox &box, std::array<int,3> &position)
    {
        this->placed_boxes.push_back(box);
        box.putOnPos(position);
    }
        
AbstractContainer::AbstractContainer(std::array<int,3> &size)
    {
        this->set_size(size);
    }

std::vector<AbstractBox> AbstractContainer::get_boxes()
    {
        return this->placed_boxes;
    }




// int main()
// {
//     std::array<int,3> size = {5,5,5};
//     std::array<int,3> pos = {1,1,1};
//     std::array<bool,3> rotatable = {true,true,true};
//     AbstractBox box1(pos, rotatable);
//     AbstractBox box2(pos, rotatable);
    
//     AbstractContainer cont(size);

//     cont.put(box1, pos);
//     cont.put(box2, pos);

//     auto boxes = cont.get_boxes();
//     // std::cout << boxes.front().get_id() << std::endl;
//     for(auto i: boxes)
//     {
//         std::cout << i.get_id() << std::endl;
//     }

//     return 0;
// }