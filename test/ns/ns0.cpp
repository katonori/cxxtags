#include "ns0.h"
namespace NS0 {
    int C0::check()
    {
        printf("C0: val is %d\n", m_val);
        return m_val;
    }
    MYINT C1::check() const
    {
        printf("C1: val is %d\n", m_val);
        return m_val;
    }
    C1 C1::check2()
    {
        return *this;
    }
    void asdf(void) {
        printf("asdf0\n");
    }
    void asdf(int a) {
        printf("asdf: %d\n", a);
    }
}
