// not actually a python example, just a binary which prints the python version which was found by cmake.

#include <cstdio>
#include <cstdlib>

#include "admt/admt.h"

int main(int argc, char* argv[]) {
    // print the python version which was defined in a macro.
#if defined(PYTHON_VERSION_MAJOR) && defined(PYTHON_VERSION_MINOR)
    printf("python %d.%d\n", PYTHON_VERSION_MAJOR, PYTHON_VERSION_MINOR);
    return admt(EXIT_SUCCESS);
#endif
    return EXIT_FAILURE;
}
