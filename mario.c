 #include <cs50.h>
#include <stdio.h>
   // To get user input
int main(void)
    // Ask user for height.
{
    int i = get_int("Height of pyramid: ");

    // Ask again if user input is incorrect.
    while (i < 1 || i > 9)
    {
        i = get_int("Height of pyramid: ");
    }
     // Display pyramid according to user's desired height. 
    for ( int k= 0; k<i; k++)
    {
         for (int c = 0; c< i-k-1; c++)
        {
            printf(" ");
        }
        
        for (int j = 0; j < k+1; j++)
        {
            printf("#");
        }
        printf("\n");
     }
}

