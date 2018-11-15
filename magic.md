# Like Magic

## Questions

4.1. 0x42 in ASCII characters = B , 0x4d in ASCII characters = M therefore string = BM

4.2. 0x25 = %, 0x50 = P , 0x44 = D, 0x46 = F therefore string = %PDF

4.3. Because the hexadecimal magic numbers are commonly the ASCII equivalent of the letters that make up the file type, though this is not always the case for example a plain text file, which does not have magic numbers.

4.4. When Zamyla reads into the file, she is taking chunks of data of 512 bytes and loading it into a temporary buffer array.
     She indexes into the buffer and checks the first three terms of the buffer to see if they all match with the first three bytes that are indicative of the jpeg file respectively, using &&.
     Finally, she checks the fourth byte at position buffer[3]. She uses the fact that all of the 16 bytes start with 0xe, which is 1110. Using the bitwise AND, she knows that if the byte at position buffer[3] is one of the bits she is looking for, that bit, compared to
     0xf0, should return 1 where both bits in that byte and bits in 0xf0 are equal to one. The first three bits of buffer[3] and 0xf0 have to match with each other so that the result gives 111. The remaining five bits should not match with any bits in 0xf0,
     such that the result is 00000, making the final result 11100000, which is 0xe0. This is only true if the byte at buffer[3] is one of the 16 bytes unique to a jpeg file. If the first 3 bytes match the first 3 bytes unique to a jpeg file, and the fourth byte satisfies the condition set using the bitwise AND,
     then the file is definitely jpeg.

4.5. Using logical OR means the computer has to check the byte at buffer[3], against all the 16 different possibilities that byte it could be to find a match.
     this has a longer runtime than zamyla's code, which checks the byte at buffer[3] for the specific condition only once and can make a conclusion.

4.6. See `magic.c`.

## Debrief

a. CS50 course's website, Google

b. 120 minutes
