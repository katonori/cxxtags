#include <stdio.h>

struct S0 {
    int a;
    int b;
    int c;
};
union U0 {
    int   a;
    short b;
    float c;
};
class C0 {
    int   a;
};
enum E0 {
    EVAL,
};

int main()
{
    S0 a;
    a.a = 0;
    a.b = 1;
    a.c = 2;
    U0 b;
    b.a = 0;
    b.b = 1;
    b.c = 1.0;
    C0 c;
    c.a = EVAL;
    return 0;
}
