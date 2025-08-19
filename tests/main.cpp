#include "admt/admt.h"

int main(int argc, char* argv[]) {
    // Check the method returns an expected value. This is a very fake test suite target.
    int result = admt(12);
    return result == 12 ? 0 : 1;
}
