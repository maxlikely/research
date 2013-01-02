
def unk(words):
    '''
    Replaces the first occurence of every word with UNK.
    '''
    unked_words = set([])

    for word in words:
        if word in unked_words:
            yield word
        else:
            unked_words.add(word)
            yield '<UNK>'
