
from nltk.corpus import propbank, BracketParseCorpusReader
from nltk.classify.naivebayes import NaiveBayesClassifier

wsj_root= r'/Users/maxlikely/data/penn_treebank/treebank-3/parsed/mrg/wsj'
file_pattern = r".*/wsj_.*\.mrg"



my_treebank = BracketParseCorpusReader(wsj_root, file_pattern)
def get_tree(instance):
    '''Helper function for loading'''
    fileloc = '%s/%s'%(instance.fileid[4:6], instance.fileid)
    tree = my_treebank.parsed_sents(fileids=fileloc)[instance.sentnum]
    return tree

