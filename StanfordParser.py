from pyquery import PyQuery
import path
import os

class StanfordParser(PyQuery):

    def parse_tokens(self):
        '''

        Extracts tokenized text from a PyQuery. Returns a list of tokenized sentences.  Each
        sentence is a list of tokens.  Each token is a dictionary with:
            word, lemma, POS, NER, CharacterOffsetBegin, CharacterOffsetEnd

        '''

        def parse_token(token):
            '''
            Parses a token from pyquery into a dictionary
            '''

            t = {}

            try:

                attributes = token.text().split()
                t['word']  = attributes[0]
                t['lemma'] = attributes[1]
                t['POS']   = attributes[4]
                t['NER']   = attributes[5]
                t['CharacterOffsetBegin'] = int(attributes[2])
                t['CharacterOffsetEnd']   = int(attributes[3])

            except:

                print 'ERROR', token

            return t

        sentences = [StanfordParser(sent) for sent in self('tokens')]
        tokenized = [[StanfordParser(token) for token in sent('token')] for sent in sentences]
        return [[parse_token(t) for t in tokens] for tokens in tokenized]

    def parse_parsetrees(self):
        '''
        Extracts parsetrees from XML. Returns a single parsetree for each sentence.
        '''
        parses = [StanfordParser(p).text().strip() for p in self('parse')]

        return parses

    def parse_dependencies(self):
        '''
        Returns a list of dependency parses. Each element corresponds to one
        sentence and each sentence is a list of dependencies.
        '''

        def parse_dependency(dep):
            '''
            Parses an individual dependency into a dictionary
            '''

            d = {}
            d['type'] = dep.attr('type')
            d['governor']  = dep('governor').text()
            d['dependent'] = dep('dependent').text()
            d['governor_idx']  = dep('governor').attr('idx')
            d['dependent_idx'] = dep('dependent').attr('idx')

            return d

        sentences    = [StanfordParser(sent) for sent in self('basic-dependencies')]
        dependencies = [[StanfordParser(dep) for dep in sent('dep')] for sent in sentences]
        return [[parse_dependency(d) for d in deps] for deps in dependencies]

    def parse_coreferences(self):
        '''
        Returns a graph of coreferences and all
        co-referent mentions.
        '''

        def parse_mention(mention):
            '''
            Parses a mention and returns a dictionary.
            '''

            m = {}
            try:
                m = {}
                text = mention.text().split()
                m['sentence'] = text[0]
                m['start'] = text[1]
                m['end'] = text[2]
                m['head'] = text[3]
            except:
                print 'error parsing mention'

            return m

        coreferents = []

        for coreferent in self('coreference'):
            coref = []
            for mention in StanfordParser(coreferent)('mention'):
                coref.append(parse_mention(StanfordParser(mention)))
            coreferents.append(coref)

        return coreferents

def process_directory(path_to_xml='.'):
    '''
    Walks through a directory of XML files produced by Stanford CoreNLP and
    parses them into Python objects. :)
    '''

    parse_dir = path.path(path_to_xml)
    filenames = parse_dir.files()

    parses = []

    for filename in filenames:
        print 'processed: %s' % filename
        try:

            sp = StanfordParser(open(filename).read())
            parses.append({'filename': filename,
                           'tokens': sp.parse_tokens(),
                           'parsetrees': sp.parse_parsetrees(),
                           'dependencies': sp.parse_dependencies(),
                           'coreferences': sp.parse_coreferences()})

        except:

            print 'errored processsing: %s' % filename

    return parses
