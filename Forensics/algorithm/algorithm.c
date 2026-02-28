#include <stdio.h>
#include <stdlib.h>

unsigned char codedChar(int bit_position, unsigned char flag_char, unsigned char bmp_char) {
    unsigned char result = flag_char;
    if (bit_position != 0) {
        result = flag_char >> bit_position;
    }
    return (bmp_char & 0xFE) | (result & 0x01);
}

int main(void) {
    char flag_char;
    char encoded_char;
    int fread_result;
    int i, j;
    int loop_count = 2000;
    FILE *flag_file;
    FILE *original_bmp;
    FILE *encoded_bmp;
    char flag_buffer[56];

    flag_file = fopen("flag.txt", "r");
    original_bmp = fopen("original.bmp", "r");
    encoded_bmp = fopen("encoded.bmp", "a");

    if (flag_file == NULL) {
        puts("No flag found, please make sure this is run on the server");
    }
    if (original_bmp == NULL) {
        puts("original.bmp is missing, please run this on the server");
    }

    fread_result = fread(&flag_char, 1, 1, original_bmp);
    for (i = 0; i < loop_count; i++) {
        fputc(flag_char, encoded_bmp);
        fread_result = fread(&flag_char, 1, 1, original_bmp);
    }

    fread_result = fread(flag_buffer, 50, 1, flag_file);
    if (fread_result < 1) {
        puts("flag is not 50 chars");
        exit(0);
    }

    for (i = 0; i < 50; i++) {
        for (j = 0; j < 8; j++) {
            encoded_char = codedChar(j, (unsigned char)(flag_buffer[i] - 5), (unsigned char)flag_char);
            fputc(encoded_char, encoded_bmp);
            fread(&flag_char, 1, 1, original_bmp);
        }
    }

    while (fread_result == 1) {
        fputc(flag_char, encoded_bmp);
        fread_result = fread(&flag_char, 1, 1, original_bmp);
    }

    fclose(encoded_bmp);
    fclose(original_bmp);
    fclose(flag_file);

    return 0;
}