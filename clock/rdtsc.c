#include <stdio.h>
#include <stdlib.h>
#include "rdtsc.h"

int main(int argc, const char *argv[])
{
    printf("%lld\n", rdtsc());
    return 0;
}
