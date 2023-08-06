# This is a module which returns the list of all things which can be done with the package
# This is inside module saeli

def Package():
    return 'Hey First Package! \n Here are the things you could do with this package'

def Add(x, y):
    if (type(x) == int) == (type(y) == int):
        return x+y
    raise Exception("Error: This idiotic trivial function takes only type(int)!")

