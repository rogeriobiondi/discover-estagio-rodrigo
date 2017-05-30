# Second Solution to Walk, Drive, Fly, problem
# In this approaching I decided to cover lists and functions
# Python Succinctly.pdf - Page 69

options = [[3,'walking'],[300, 'driving'],[4000,'flying'],[16000,'rocketing']]
options.append([50000,'interdimensional traveling'])

def suggestion(miles):
    """Choose the better transportation for given miles."""

    # To work with arrays, you don't need to set range
    # But to iterate inside a list, you must set it.
    for x in range(len(options)):
        if miles < options[x][0]:
            return print("I suggest you {} to your destination!".format(options[x][1]))
        else:
            return print("Sorry, I think you'll not reach your destination too soon!")

distance = input("How many miles? ")
suggestion(int(distance))

