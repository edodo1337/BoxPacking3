#pragma once

#include <array>
#include <vector>
#include "abstract_box.h"

class AbstractContainer
{
    private:
        std::array<int,3> size;
        std::vector<AbstractBox> placed_boxes;
    
    public:
        void set_size(std::array<int,3> &size);
        void put(AbstractBox &box, std::array<int,3> &position);
        std::vector<AbstractBox> get_boxes();
        AbstractContainer(std::array<int,3> &size);

};