#Get a value in dictionary according to a formated key like so : parent.child1.child2
def getInDict(dictionary, formated_key):
    try:
        nodes = formated_key.split('.')
        pointer = dictionary[nodes[0]]
        #go deep to retreive the corresponding value
        for node in nodes[1:]:
            pointer = pointer[str(node)]
    except KeyError: #key is wrong set the output to none
        pointer = None
    return pointer
