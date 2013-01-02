
import fileinput
import multiprocessing
import nltk

from nltk.stem.wordnet import WordNetLemmatizer

porter = nltk.PorterStemmer()
stopwords = nltk.corpus.stopwords.words('english')
lmtzr = WordNetLemmatizer()

def process_doc(doc, min_length=3):
    """This processes a single doc and return a normalized list of its tokens.

    :param doc: The document to process
    :type doc: str.
    :returns:  list -- the list of tokens

    """

    toks = nltk.wordpunct_tokenize(doc.strip().lower())
    toks = filter(lambda x: len(x) >= min_length, toks)
    toks = filter(lambda x: x not in stopwords + ['dear', 'sir', 'madam'], toks)
    #toks = [porter.stem(x) for x in toks]
    toks = [lmtzr.lemmatize(x) for x in toks]

    return toks

def process_docs(docs, threads=False):
    """
    This pooling bit is adapted from Michael Bommarito's `comparison
    <http://bit.ly/eQaWwz>` of R's tm and python's NLTK. Now I can use
    threads!

    """

    #pool   = multiprocessing.Pool(8)
    #if threads:
    #    corpus = pool.map(process_doc, docs)
    #else:
    corpus = [process_doc(d) for d in docs]

    #"""Write all this goodness to an output file of the format
    #0 doc1word1 doc1word2 ...
    #0 doc2word1 doc2word2 ...

    #The integer at the start is conforms to MJP's TAM, LDA, ccLDA
    #expected input.

    #"""
    #f = open('out.txt', 'w')
    #for doc in corpus: f.write(str(0) + ' ' + ' '.join(doc) + '\n')
    #f.close()

    return corpus
