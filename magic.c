#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check if there are only 2 command line arguments
    if (argc != 2)
    {

        fprintf(stderr, "Usage: name of forensic image\n");
        return 1;

    }
// Remember input filename
    char *file = argv[1];

// Open input file
    FILE *inptr = fopen(file, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", file);
        return 1;

    }

// Creating buffer array
    uint8_t buffer[4];
// Read into file
    while (fread(buffer, 4, 1, inptr) == 1)
    // Check if file is bmp file
        if (buffer[0] == 0x42 && buffer[1] ==0x4d)
        {
            printf("BMP\n");
        }
    // Check if file is jpeg file
        else if (buffer[0] == 0xff &&
                 buffer[1] == 0xd8 &&
                 buffer[2] == 0xff &&
                (buffer[3] & 0xf0) == 0xe0)
        {
            printf("JPEG\n");
        }
    // Check if file is pdf
        else if (buffer[0] == 0x25 && buffer[1]  == 0x50 && buffer[2] == 0x44 && buffer[3] == 0x46)
        {
            printf("PDF\n");
        }

        fclose(inptr);

// Program Success
    return 0;
}