#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c);
int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
  
    for (int i = 0; i < strlen(argv[1]); i++)
        if (!isalpha(argv[1][i]))
        {
            printf("Usage: ./vigenere keyword\n");
            return 2;
        }
    // To declare variables
    int count = 0;
    int length = strlen(argv[1]);
    int key = shift(argv[1][count]);
    printf("%i\n", key);
    
    // To get plaintext from user     
    string s = get_string("Plaintext: ");
    printf("Ciphertext: ");
    for (int i = 0; i < strlen(s); i++)
    {
        int c = (int)s[i]; 
        if (count < strlen(argv[1]))    
        {   
            printf("%c", c + count);
            count++;
        }
        // To encrypt code
        else 
        {
            if (count == length)
            {
                count = 0;
                printf("%c", c);
                count ++;
            }
            
            else
            {
                printf("%c", c);
            }
        }
    }
    
    printf("\n");
}

// To declare shift function               
int shift(char c)
{
    if (isupper(c))
    {
        int A = c - 'A';
        return A;
    }
    else
    {
        int a = c - 'a';
        return a;
    }
}
