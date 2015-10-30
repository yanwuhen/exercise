#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

void test(int a, ...) {
    int j;
    va_list arg;
    va_start(arg, a);
    j = va_arg(arg, int);
    printf("j:%d\n", j);
    j = va_arg(arg, int);
    printf("j:%d\n", j);
    va_end(arg);
}
int main(int argc, const char *argv[])
{
    test(1, 2, 3);
    return 0;
}
