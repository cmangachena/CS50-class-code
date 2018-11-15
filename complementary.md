# Complementary Questions

## Questions

1.1. 10000011 by writing it as the normal 3 in binary then changing the leftmost bit to 1

1.2. 3 in binary is 00000011, inverting all the ones to zeros: 11111100,
     then adding 1, (00000001), -3 in binary = 11111101

1.3. If the counter had been allocated a restricted number of bits, if the counter goes up to 11111111 in binary for example, it would have reached the maximum of positive numbers it can record.
     11111111 happens to be the same binary representation of -1 in bits too therefore the computer might interpret it like that as well.

1.4. the data type - 'int' has a memory allocation of 4 bytes. It can represent numbers from -2,147,483,648 to 2,147,483,647. When counter got to the maximum, it could not represent 2,147,483,648, the highest number it had to show, but that same number's binary notation is the same as it's negative form,
     so the computer ended up representing that instead. When it tried to multiply that negative number by 2, the counter broke because the int data type became too small to represent the result of that multiplication and then ended up just showing zeros.
1.5. They had used allocated 16-bits to a data-type in which they needed to store data, the data the rocket in flight ended up generating needed a data type with 64 bits instead to be stored. As a result the data could not be stored and the rocket became faulty.

## Debrief

a. Google, cs50 sandbox, cs50 lecture notes

b. 60 minutes
