// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdint.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}
//Declare a counter for keeping track of words in dictionary
int counter = 0;
// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];
    //
    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        node *Newnode = malloc(sizeof(node));
        strcpy(Newnode->word, word);
        node *main = hashtable[hash(word)];
        Newnode->next = main;
        hashtable[hash(word)] = Newnode;

        counter ++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return counter;
}

// Returns true if word is in dictionary else false


bool check(const char *word)
{
    // Save index of current word to be checked
    int cur_word = hash(word);
    // Make index equal to address
    node *ad1 = hashtable[cur_word];
    // Check for every word
    while (ad1 != NULL)
    {
        node *ad2 = ad1->next;
        // Make sure the result is true regardless of case
        if (strcasecmp(ad1->word, word) == 0)
        {
            return true;
        }
        ad1 = ad2;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int j = 0; j < 26; j++)
    {
        // Creating a way to iterate over nodes
        node *ad1 = hashtable[j];

        while (ad1 != NULL)
        {
            // Save next address
            node *ad2 = ad1;
            ad1 = ad1->next ;
            // Destroy node
            free(ad2);
        }
    }
    return true;
}
