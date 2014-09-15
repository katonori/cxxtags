#include <stdio.h>

enum {
    VAL0_0,
    VAL0_1,
    VAL0_2,
    VAL0_3,
};

enum {
    VAL1_0,
    VAL1_1,
    VAL1_2,
    VAL1_3,
};

static void check()
{
    printf(":: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
}

namespace NS0 {
    enum {
        VAL0_0=10,
        VAL0_1,
        VAL0_2,
        VAL0_3,
    };
    static void check()
    {
        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
    }
    class C0 {
        public:
        enum {
            VAL0_0 = 20,
            VAL0_1,
            VAL0_2,
            VAL0_3,
        };
        void check()
        {
            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
        }
    };
    class C1 : public C0
    {
        public:
        enum {
            VAL0_0 = 30,
            VAL0_1,
            VAL0_2,
            VAL0_3,
        };
        void check()
        {
            printf("NS0::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
        }
    };
};

namespace NS1 {
    enum {
        VAL0_0 = 40,
        VAL0_1,
        VAL0_2,
        VAL0_3,
    };
    static void check()
    {
        printf("NS0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
    }
    class C0 {
        public:
        enum {
            VAL0_0 = 50,
            VAL0_1,
            VAL0_2,
            VAL0_3,
        };
        void check()
        {
            printf("NS0::C0:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
        }
    };
    class C1 : public C0
    {
        public:
        void check()
        {
            printf("NS1::C1:: %d, %d, %d, %d\n", VAL0_0, VAL0_1, VAL0_2, VAL0_3);
        }
    };
};

int main()
{
    NS0::C0 c00;
    NS0::C1 c01;
    NS1::C0 c10;
    NS1::C1 c11;
    ::check();
    NS0::check();
    NS1::check();
    c00.check();
    c01.check();
    c10.check();
    c11.check();
}

enum namedEnum {
    VAL2_0,
    VAL2_1,
};
namedEnum e = VAL2_1;
