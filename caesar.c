
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{  
    // To check if program was run with one command line.
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // Convert characters to intergers
    int key = atoi(argv[1]);
    // If user did not input digits in key
    if (key == 0)
     { 
        printf(" Usage: ./caesar key\n");
        return 2; 
     }  
   else
    {
      printf("\n");
    }
    // Prompt user for plaintext
    string s = get_string("Plaintext: ");
    printf("\n");
    
   // Print out ciphertext
    printf("Ciphertext: ");
    
     for(int i = 0; i < strlen (s); i++)
    {
        // To convert string to integer
         int c = (int) s[i];
         
        // To preserve uppercase
         if (c <=97 && c>= 65)    
        {   
         printf("%c", ((c-65 + key)%26) + 65);
        }
        // To preserve lowercase
        else 
        {
             if(c <= 122 && c >= 97)
             {
                printf("%c", (( c-97 + key)%26) + 97);
             }
             // To preserve punctuation
          else
            {
                printf("%c", c);
            }
        }
     }
    
    printf("\n");
}



                   

