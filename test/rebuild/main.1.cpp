#include <stdio.h>

class CParent0
{
    public:
    CParent0(){}
    ~CParent0(){}
    virtual void response(void);
};

void CParent0::response(void) {
    printf("parent0\n");
}

class CParent1
{
    public:
    CParent1(){}
    ~CParent1(){}
    virtual void response(void);
};

void CParent1::response(void) {
    printf("parent1\n");
}

class CChild
: public CParent0
{
    public:
    CChild(){}
    ~CChild(){}
    virtual void response(void);
};

void CChild::response(void) {
    printf("child\n");
}

class CGChild
: public CChild
{
    public:
    CGChild(){}
    ~CGChild(){}
    virtual void response(void);
};

void CGChild::response(void) {
    printf("gchild\n");
}

class COther
: public CParent0, public CParent1
{
    public:
    COther(){}
    ~COther(){}
    virtual void response(void);
};

void COther::response(void) {
    printf("other\n");
}

static void test(class CParent0 *a)
{
    a->response();
}

int main()
{
    CParent0 parent;
    CChild child;
    CGChild gchild;
    COther other;
    parent.response();
    child.response();
    gchild.response();
    other.response();
    test(&parent);
    test(&child);
    test(&gchild);
    test(&other);
    return 0;
}
