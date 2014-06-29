#include <vector>
#include <iostream>
#include <stdio.h>

class C0 {
public:
    C0(int a) : mVal(a) {}
    void check(void) const
    {
        printf("check: %d\n", mVal);
    }
private:
    int mVal;
};

template <typename in_type >
void func_test(in_type val)
{
    std::cout << "out: " << val << std::endl;
}

int main()
{
    func_test(1);
    func_test(2.2);
    std::vector<C0 > vecTest;
    for(int i = 0; i < 8; i++) {
        vecTest.push_back(C0(i));
    }
    for(std::vector<C0 >::iterator itr = vecTest.begin();
        itr != vecTest.end();
        itr++) {
        itr->check();
    }
    return 0;
}

// TODO: add more test
