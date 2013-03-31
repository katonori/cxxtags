#include <vector>
#include "ns0.h"
#include "ns1.h"

#define BUFF_SIZE 256
char msg[BUFF_SIZE] = "MESSAGE\n";
int main()
{
    std::vector<int > vec;
    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);
    NS0::C0 c00(0);
    NS1::C0 c10(1);
    NS0::C1 c01(2);
    NS1::C1 c11(3);
    c00.check();
    c10.check();
    c01.check();
    c11.check();
    printf("AAA: %s\n", msg);
    for(std::vector<int >::iterator i = vec.begin();
    i != vec.end();
    i++){
        printf("%d\n", *i);
    }
    return 0;
}
