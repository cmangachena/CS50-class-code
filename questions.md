# Questions

## What's `stdint.h`?

It is a header file that enables us to get extra functions for ingers.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

To define the type of data we will be using, it defines an unsigned integer from 0 and up.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

a BYTE is 1 byte and it is 8-bits lonh
a DWORD is 4 bytes long, 32-bits
a LONG is 4 bytes long, or 32-bits
a WORD is 2 bytes long, or 16 bits


## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."


bm

## What's the difference between `bfSize` and `biSize`?

bfSize is the size of the whole file,while biSize is the size of the bitmapinfofile header.

## What does it mean if `biHeight` is negative?

It means the image is upside down or stored from top to bottom.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

Because the file that one is trying to open might not exist.

## Why is the third argument to `fread` always `1` in our code? (For example, see lines 40, 44, and 75.)

Third argument represents the quantity of blocks so 1 means that fread will be reading one block of code (1 byte), at a time

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
it assigns : ((4 - (3 x 3))%4)%4 it would assign 0.

## What does `fseek` do?

moves the file position to the user's desired positin within the file

## What is `SEEK_CUR`?

it specifies the current position of the file.

(consulted google and microsoft website)
