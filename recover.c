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
    char *image = argv[1];

// Open input file
    FILE *inptr = fopen(image, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", image);
        return 2;

    }

// Creating buffer array
    uint8_t buffer[512];


// Initialize variables

    int jpegposition = 0;

// To search for the start of a JPEG

    while (fread(buffer, 512, 1, inptr) == 1)
    {
        //printf("While\n");
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
        {
            printf("Yes\n");
            char filename[8];
            // Create filename
            sprintf(filename, "%03d.jpg", jpegposition);
            FILE *outptr = fopen(filename, "w");
            // Writing the first chunk
            fwrite(buffer, 512, 1, outptr);
            fread(buffer, 512, 1, inptr);

            while (buffer[0] != 0xff && buffer[1] != 0xd8 && buffer[2] != 0xff)
            {
                fwrite(buffer, 512, 1, outptr);
                fread(buffer, 512, 1, inptr);

            }
            // Correcting alignment
            fseek(inptr, -512, SEEK_CUR);
            jpegposition++;
            fclose(outptr);
        }
    }
    fclose(inptr);

// Program Success
    return 0;

}