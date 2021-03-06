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
#include "libgls.h"

// using namespace boost::numeric::ublas;

int main()
{
    
    std::array<int,3> pos1{4,4,4};
    std::array<int,3> diag1{5,5,5};
    std::array<int,3> size1{5,5,5};

    std::array<int,3> pos2{5,5,5};
    std::array<int,3> diag2{2,2,2};
    std::array<int,3> size2{2,2,2};

    std::array<bool,3> is_rotatableXYZ{true, true, true};
    
    AbstractBox box1 = AbstractBox(size1, is_rotatableXYZ);
    AbstractBox box2 = AbstractBox(size2, is_rotatableXYZ);

    box1.putOnPos(pos1);
    box2.putOnPos(pos2);

    box1.set_diag(diag1);
    box2.set_diag(diag2);


    clock_t tStart = clock();
    std::array<bool,3> *b = check_boxes_intersect(box1, box2);

    // std::cout << (*b)[0] << std::endl;
    printf("Time taken: %.10fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
    
    return 0;
}