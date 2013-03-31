#include <stdio.h>
namespace NS0 {
    typedef int MYINT ;
    class C0 {
        public:
        C0(int a) : m_val(a) {}
        int check();
        private:
        int m_val;
    };
    class C1 {
        public:
        C1(int a) : m_val(a) {}
        MYINT check() const;
        C1 check2();
        private:
        int m_val;
    };
};

