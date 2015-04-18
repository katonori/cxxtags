void func();
void func()
{
    return;
}

#define FUNC func

int main()
{
    FUNC();
    func();
    return 0;
}
