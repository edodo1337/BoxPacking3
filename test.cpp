#include <iostream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <array>
#include <numeric>
// #include <boost/lambda/lambda.hpp>
// #include <boost/numeric/ublas/vector.hpp>
// #include <boost/numeric/ublas/matrix.hpp>
// #include <boost/numeric/ublas/io.hpp>
// #include <boost/numeric/ublas/assignment.hpp>
#include <time.h>
#include "utils.h"
#include "abstract_box.h"
#include "abstract_container.h"

// using namespace boost::numeric::ublas;

int main()
{
   

    // std::array<int,3> size{1,2,3};
    // std::array<int,3> pos{0,0,0};
    // std::array<bool,3> is_rotatableXYZ{true,true,true};

    // AbstractBox box = AbstractBox(size, is_rotatableXYZ);

    // std::vector<std::array<int,3>> ps{{0,0,0}};
    // std::array<int,3> cont_size = {10,10,10};
    // AbstractContainer cont = AbstractContainer{cont_size};
    // // cont.put(box, pos);

    // std::vector<AbstractBox> boxes;
    // // boxes.reserve(10);

    // for (int i(0); i<1000; i++)
    // {
    //     AbstractBox box = AbstractBox(size, is_rotatableXYZ);
    //     boxes.push_back(box);
    // }
    
    clock_t tStart = clock();
    // for (auto i:boxes)
    // {
    //     i.rotateX();
    //     cont.put(i, pos);
    // }
    // int vp[3] = { size[0], size[1], size[2]};
    // for (auto v:vp)
    //     std::cout<<v;

    
    std::array<int,2> ar1{2,1};
    std::array<int,2> ar2{3,8};

    
    std::array<int,2> result = {
        std::min(ar1[0], ar1[0]+ar2[0]),
        std::max(ar1[0], ar1[0]+ar2[0]), 
    };   



    for (auto i:result)
        std::cout<<i << " ";
    printf("Time taken: %.10fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    
    return 0;
}