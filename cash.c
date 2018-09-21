#include <math.h>
#include <cs50.h>
#include <stdio.h>
int main (void)
{
    float change = get_float("Change required: ");
    while ( change < 0 )
    { 
        change = get_float("Change required: ");
    }
    // Converting dollars to cents.
    int change_required = round(change * 100);
    // Calculating change required.
    int quarters= change_required/25;
    int dimes = (change_required - quarters*25)/10;
    int nickels = (change_required - (quarters*25 + dimes*10))/5;
    int pennies = (change_required - (quarters*25 + dimes*10 + nickels*5));
    int total = (quarters + dimes + nickels + pennies);
    // Printing coins required.
    printf("Coins required = %i\n" , total);
} 
