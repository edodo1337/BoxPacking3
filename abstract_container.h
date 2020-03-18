#pragma once

#include <vector>
#include <array>
// #include <boost/numeric/ublas/vector.hpp>
// #include <boost/numeric/ublas/assignment.hpp>
#include "abstract_box.h"
// using namespace boost::numeric::ublas;

class AbstractContainer
{
    private:
        std::array<int,3> size;
        std::vector<AbstractBox> placed_boxes;
        std::vector<std::array<int,3>> points{{0,0,0}};
        
    public:
        void set_size(std::array<int,3> &size);
        void put(AbstractBox &box, std::array<int,3> &position);
        std::vector<AbstractBox> get_boxes();
        AbstractContainer(std::array<int,3> &size);
};