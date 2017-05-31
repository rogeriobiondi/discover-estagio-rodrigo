# Exercise 'Fill the blank words', page 79
# Read user inputs and creates a story with that
#Included option to save to disk with path.


import os

stories = open('./Story.txt', 'w+')

def get_word(word_class):
    """Get a word from standard input and return it."""

    if word_class.lower() == 'adj':
        article = 'an'
    else:
        article = 'a'

    return input("Enter a word that is {0} {1}".format(article, word_class))


def filler(noun, verb, adj):
    """Write the story filling with the user input"""
    story = "I never knew anyone that hadn't {1} at least once in their life, except for {2}, old Aunt Polly. She never {1}, not even when that {0} came to town.".format( noun, verb, adj)
    return story

def printer(story, svdsk):
    """Print the Story: 0 stdout, 1 file"""
    print()

    print()
    if svdsk.lower() == 'yes' or svdsk.lower() == 'y':
        print(story, file=stories)
        if os.path.isfile('./Story.txt'):
            print('\/ Enjoy! \/ ')
            print(os.path.abspath('./Story.txt'))
        else:
            print("Something gone wrong! No file recorded!")
    else:
        print('\/ Enjoy! \/ ')
        print(story)
        stories.close()

def create_story():
    noun = get_word('noun')
    verb = get_word('verb')
    adj = get_word('adj')

    option = input("Want to save your Story to your disk? Type '[Y]es' or nothing to just Read it. ")

    filled_story = filler(noun, verb, adj)
    printer(filled_story, option)

create_story()

