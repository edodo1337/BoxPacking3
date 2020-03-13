#include <iostream>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/vector.hpp>
using namespace boost::numeric::ublas;

#include "inverse.h"
//////////////////////////////////////////////////////////////////////////////
// вывод на экран матрицы 2х2
void print_matrix_2_2(const std::string& sText, boost::numeric::ublas::matrix<double> a)
{
    std::cout<<sText<<std::endl;
    std::cout<<a(0,0)<<" "<<a(0,1)<<std::endl;
    std::cout<<a(1,0)<<" "<<a(1,1)<<std::endl<<std::endl;    
}
/////////////////////////////////////////////////////////////////////////////
void main()
{
    // Начальная инициализация матрицы a
    boost::numeric::ublas::matrix<double> a(2,2);
    a(0,0)=1.;
    a(0,1)=2.;
    a(1,0)=3.;
    a(1,1)=4.;
    print_matrix_2_2("a:", a);

    // матрица b - единичная
    boost::numeric::ublas::matrix<double> b(2,2);
    b(0,0)=1.;
    b(0,1)=0.;
    b(1,0)=0.;
    b(1,1)=1.;
    print_matrix_2_2("b:", b);

    // перемножение двух матриц
    boost::numeric::ublas::matrix<double> c = prod(b, a);
    print_matrix_2_2("c=a*b:", c);

    // результат обращения матрицы a записан в матрицу b
    bool flag = false;
    b=gjinverse<double>(a, flag);

    print_matrix_2_2("b=invert a:", b);

    // перемножение матрицы a и обратной ей матрицы = единичная матрица
    c = prod(b, a);
    print_matrix_2_2("c=b*a:", c);
}