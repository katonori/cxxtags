#include <iostream>
#include <b.h>
namespace proja {
#ifndef MUSTDEF
#error "DEFFINE"
#endif
void func()
{
    std::cout << "proja::func0" << std::endl;
    projb::func();
}
};
int main()
{
    proja::func();
    return 0;
}
