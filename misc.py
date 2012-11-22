def pair_generator(conditions):
    '''
    Generates all pairs of a list
    '''
    for condition1 in conditions:
        for condition2 in conditions:
            yield (condition1, condition2)

