// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    // ensure correct range of n
    int n = atoi(argv[1]);
    if (n > 100 || n <= 0)
    {
        fprintf(stderr, "n must be greater than zero and n is less than or equal to 100 \n");
        return 4;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

//Declare and identify significant variables
    int oldWidth = bi.biWidth;
    int oldHeight = bi.biHeight;
    int oldpadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    //Increase size of biHeight and biWidth according to user's desired scale
    bi.biWidth = n * (oldWidth);
    bi.biHeight = n * (oldHeight);

    //Calculation of new padding for rows
    int newpadding = ((4 - bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = (bi.biWidth * sizeof(RGBTRIPLE) + newpadding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // Write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // Write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    // Iterate over infile's row
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // temporary buffer
        RGBTRIPLE triple;

        // Iterate over each pixel in row

        for (int b = 0; b < oldWidth; b++)
        {
            // Read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
        }
        // To enlarge image
        for (int a = 0; a < n ; a++)
        {
            for (int d = 0; d < oldHeight ; d++)
            {

                for (int e = 0; e < n ; e++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), n + 1, outptr);
                }
                fwrite(&triple, sizeof(n * oldHeight), n + 1, outptr);
            }
            //Increment old padding
            for (int f  = 0; f < oldpadding; f++)
            {
                fputc(0x00, outptr);
            }
        }

        // Check for padding and if any, skip over it
        fseek(inptr, oldpadding, SEEK_CUR);

        // Finally add newpadding back:
        for (int m = 0 + n; m < oldpadding; m++)
        {
            fputc(0x00, outptr);
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
