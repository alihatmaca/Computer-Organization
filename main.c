/* Haydar Ali Atmaca, 5001230016, G2 */
const int SID = 1230016;
int notlar[40];
int bucket[5];
int mean = 0, below_count = 0, pass_count = 0;

int grup(int g) {
    if (g < 50) return 0;
    if (g < 65) return 1;
    if (g < 75) return 2;
    if (g < 85) return 3;
    return 4;
}

int main(void) {
    unsigned int x = SID;
    int toplam = 0;
    int P = 50 + (SID % 10);

    for (int i = 0; i < 40; i++) {
        x = 1664525u * x + 1013904223u;
        notlar[i] = (x >> 16) % 101;
    }

    for (int i = 0; i < 40; i++) {
        toplam += notlar[i];
        bucket[grup(notlar[i])]++;
        if (notlar[i] >= P)
            pass_count++;
    }
    mean = toplam / 40;

    for (int i = 0; i < 40; i++) {
        if (notlar[i] < mean) {
            notlar[i] = notlar[i] | 0x100;
            below_count++;
        }
    }
    return 0;
}
