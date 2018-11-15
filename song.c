#include <cs50.h>
#include <stdio.h>

void recursion():
{
    printf("This is the song that doesn't end.");
    printf("Yes, it goes on and on my friend.");
    printf("Some people started singing it not knowing what it was,");
    printf("And they'll continue singing it forever just because...");
    recursion();
}

int main (void)
{
    recursion();
}