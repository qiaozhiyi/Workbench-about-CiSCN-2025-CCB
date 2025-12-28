#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned int seed = 0x34952046;
    srand(seed);
    unsigned char key[16];
    for (int i = 0; i < 4; i++) {
        int r = rand();
        key[i*4] = r & 0xFF;
        key[i*4+1] = (r >> 8) & 0xFF;
        key[i*4+2] = (r >> 16) & 0xFF;
        key[i*4+3] = (r >> 24) & 0xFF;
    }
    for (int i = 0; i < 16; i++) {
        printf("%02x", key[i]);
    }
    printf("\n");
    return 0;
}
