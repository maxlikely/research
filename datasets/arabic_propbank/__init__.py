'''
Corpus reader for Arabic PropBank (http://verbs.colorado.edu/propbank/)

Based on the Natural Language Toolkit PropBank Corpus Reader by Edward Loper
<edloper@gradient.cis.upenn.edu>

:author David Lundgren <david.m.lundgren@gmail.com>

'''

import re
import codecs

import APBTree

from collections import namedtuple
import pickle
import APBTree

def get_raw_instances(propbank):
    '''
    Turns propbank instance into a workable dataset
    '''

    Instance  = namedtuple('Instance', 'tree arguments predicate pos sense')
    instances = []
    for (predicate_text, pos), senses in propbank.items():
        for i, (sense_gloss, abstracts, data) in enumerate(senses):
            for datum in data:

                roleset  = '%s-%s.%02d' % (predicate_text, pos, i+1)
                tree = datum[0]
                arguments = datum[1]
                print roleset

                instance = Instance(tree=tree,
                                    pos=pos,
                                    sense=sense_gloss,
                                    arguments=arguments,
                                    predicate=predicate_text)

                instances.append(instance)

    return instances

#def get_raw_instances(propbank):
#    '''
#    Turns propbank instance into a workable dataset
#    '''
#
#    Instance  = namedtuple('Instance', 'tree arguments predicate pos sense')
#    instances = []
#    for (predicate_text, pos), senses in propbank.items():
#        for i, (sense_gloss, abstracts, data) in enumerate(senses):
#            for datum in data:
#
#
#
#                #instance = ArabicPropbankInstance.parse_from_dict_item(item)
#
#
#                roleset  = '%s-%s.%02d' % (predicate_text, pos, i+1)
#                tree = datum[0]
#                arguments = datum[1]
#
#                #instance = ArabicPropbankInstance(tree, sense_gloss,
#                #        arguments, roleset, pos)
#
#                outstr = '%s\t%s\t' % (tree, roleset)
#                print outstr
#
#                #instances.append(instance)
#
#    return instances

class ArabicPropbankInstance():
    def __init__(self, tree, sense_gloss, arguments, roleset, pos):

        self.filename = 'file.name'
        '''Name of the Arabic TreeBank file containing the parse tree'''

        self.sentnum = sentnum
        """The sentence number of this sentence within ``fileid``.
        Indexing starts from zero."""

        self.wordnum = wordnum
        """The word number of this instance's predicate within its
        containing sentence.  Word numbers are indexed starting from
        zero, and include traces and other empty parse elements."""

        self.tagger = 'gold'
        """An identifier for the tagger who tagged this instance; or
        ``'gold'`` if this is an adjuticated instance."""

        self.roleset = roleset
        """The name of the roleset used by this instance's predicate.
        Use ``propbank.roleset() <PropbankCorpusReader.roleset>`` to
        look up information about the roleset."""

        self.inflection = None #inflection
        """A ``PropbankInflection`` object describing the inflection of
        this instance's predicate."""

        self.predicate = predicate
        """A ``PropbankTreePointer`` indicating the position of this
        instance's predicate within its containing sentence."""

        self.arguments = tuple(arguments)
        """A list of tuples (argloc, argid), specifying the location
        and identifier for each of the predicate's argument in the
        containing sentence.  Argument identifiers are strings such as
        ``'ARG0'`` or ``'ARGM-TMP'``.  This list does *not* contain
        the predicate."""

        self.sense_gloss = sense_gloss

        # make instance's tree a real tree
        try:
            tree_text = APBTree.fix_parse_tree_text(tree, pos)
            self.tree = APBTree.APBTree(tree_text)
        except:
            self.tree = None

    @property
    def baseform(self):
        """The baseform of the predicate."""
        return self.roleset.split('-')[0]

    @property
    def pos(self):
        """The baseform of the predicate."""
        return self.roleset.split('.')[1].split('-')[1]

    @staticmethod
    def parse(s):
        pass


def Argument(object):
    def __init__(self, label, position, text, description):
        self.label = label
        self.position = position
        self.text = text
        self.description = description

    @staticmethod
    def parse(label, arg, tree):
        text = arg[0] if '-NONE-' not in arg[0] else arg[0].split()[1]
        description = arg[1]
        position = tree.get_arg_node_position(text)

        return Argument(label, position, text, description)

    def __str__(self):
        return u'%s (%s) -- %s' % (self.text, self.description, self.label)

    def __repr__(self):
        return u'%s (%s) -- %s' % (self.text, self.description, self.label)


def clean_instance(instance):
    '''
    Gets an instance ready for feature extraction.
    '''
    try:
        # make instance's tree a real tree
        tree_text = APBTree.fix_parse_tree_text(instance.tree, instance.pos)
        instance  = instance._replace(tree=APBTree.APBTree(tree_text))

        # get arguments into useable form
        arguments = []
        Argument = namedtuple('Argument', 'label position text description')
        for (label, arg) in instance.arguments.items():
            text = arg[0] if '-NONE-' not in arg[0] else arg[0].split()[1]
            argument = Argument(label=label,
                                text=text,
                                description=arg[1],
                                position=instance.tree.get_arg_node_position(text))
            arguments.append(argument)
        instance = instance._replace(arguments=arguments)


        # fix up predicate
        Predicate = namedtuple('Predicate', 'text position')
        position  = instance.tree.get_predicate_node_position(instance.predicate, instance.pos)
        predicate = Predicate(text=instance.predicate, position=position)
        instance  = instance._replace(predicate=predicate)

    except:
        return None

    return instance

def gimme_args(returnRoleDataList):
    '''
    Returns all arguments over all senses of a predicate
    '''
    args = []
    for roleSense, argDict, frameInfoList in returnRoleDataList:
        args.append(tuple(argDict.keys()))

    return args

def load(filename='../../data/propbank.pickle'):
    '''
    Loads propbank into reasonable format.
    '''

    propbank  = pickle.load(open(filename))
    instances = get_raw_instances(propbank)

    return filter(None, [clean_instance(i) for i in instances])

######################################################################
#{ Propbank Instance & related datatypes
######################################################################

class PropbankInstance(object):

    def __init__(self, fileid, sentnum, wordnum, tagger, roleset,
                 inflection, predicate, arguments, parse_corpus=None):

        self.fileid = fileid
        """The name of the file containing the parse tree for this
        instance's sentence."""

        self.sentnum = sentnum
        """The sentence number of this sentence within ``fileid``.
        Indexing starts from zero."""

        self.wordnum = wordnum
        """The word number of this instance's predicate within its
        containing sentence.  Word numbers are indexed starting from
        zero, and include traces and other empty parse elements."""

        self.tagger = tagger
        """An identifier for the tagger who tagged this instance; or
        ``'gold'`` if this is an adjuticated instance."""

        self.roleset = roleset
        """The name of the roleset used by this instance's predicate.
        Use ``propbank.roleset() <PropbankCorpusReader.roleset>`` to
        look up information about the roleset."""

        self.inflection = inflection
        """A ``PropbankInflection`` object describing the inflection of
        this instance's predicate."""

        self.predicate = predicate
        """A ``PropbankTreePointer`` indicating the position of this
        instance's predicate within its containing sentence."""

        self.arguments = tuple(arguments)
        """A list of tuples (argloc, argid), specifying the location
        and identifier for each of the predicate's argument in the
        containing sentence.  Argument identifiers are strings such as
        ``'ARG0'`` or ``'ARGM-TMP'``.  This list does *not* contain
        the predicate."""

        self.parse_corpus = parse_corpus
        """A corpus reader for the parse trees corresponding to the
        instances in this propbank corpus."""

    @property
    def baseform(self):
        """The baseform of the predicate."""
        return self.roleset.split('.')[0]

    @property
    def sensenumber(self):
        """The sense number of the predicate."""
        return self.roleset.split('.')[1]

    @property
    def predid(self):
        """Identifier of the predicate."""
        return 'rel'

    def __repr__(self):
        return ('<PropbankInstance: %s, sent %s, word %s>' %
                (self.fileid, self.sentnum, self.wordnum))

    def __str__(self):
        s = '%s %s %s %s %s %s' % (self.fileid, self.sentnum, self.wordnum,
                                   self.tagger, self.roleset, self.inflection)
        items = self.arguments + ((self.predicate, 'rel'),)
        for (argloc, argid) in sorted(items):
            s += ' %s-%s' % (argloc, argid)
        return s

    def _get_tree(self):
        if self.parse_corpus is None: return None
        if self.fileid not in self.parse_corpus.fileids(): return None
        return self.parse_corpus.parsed_sents(self.fileid)[self.sentnum]
    tree = property(_get_tree, doc="""
        The parse tree corresponding to this instance, or None if
        the corresponding tree is not available.""")

    @staticmethod
    def parse(s, parse_fileid_xform=None, parse_corpus=None):
        pieces = s.split()
        if len(pieces) < 7:
            raise ValueError('Badly formatted propbank line: %r' % s)

        # Divide the line into its basic pieces.
        (fileid, sentnum, wordnum,
         tagger, roleset, inflection) = pieces[:6]
        rel = [p for p in pieces[6:] if p.endswith('-rel')]
        args = [p for p in pieces[6:] if not p.endswith('-rel')]
        if len(rel) != 1:
            raise ValueError('Badly formatted propbank line: %r' % s)

        # Apply the fileid selector, if any.
        if parse_fileid_xform is not None:
            fileid = parse_fileid_xform(fileid)

        # Convert sentence & word numbers to ints.
        sentnum = int(sentnum)
        wordnum = int(wordnum)

        # Parse the inflection
        inflection = PropbankInflection.parse(inflection)

        # Parse the predicate location.
        predicate = PropbankTreePointer.parse(rel[0][:-4])

        # Parse the arguments.
        arguments = []
        for arg in args:
            argloc, argid = arg.split('-', 1)
            arguments.append( (PropbankTreePointer.parse(argloc), argid) )

        # Put it all together.
        return PropbankInstance(fileid, sentnum, wordnum, tagger,
                                roleset, inflection, predicate,
                                arguments, parse_corpus)

class PropbankPointer(object):
    """
    A pointer used by propbank to identify one or more constituents in
    a parse tree.  ``PropbankPointer`` is an abstract base class with
    three concrete subclasses:

      - ``PropbankTreePointer`` is used to point to single constituents.
      - ``PropbankSplitTreePointer`` is used to point to 'split'
        constituents, which consist of a sequence of two or more
        ``PropbankTreePointer`` pointers.
      - ``PropbankChainTreePointer`` is used to point to entire trace
        chains in a tree.  It consists of a sequence of pieces, which
        can be ``PropbankTreePointer`` or ``PropbankSplitTreePointer`` pointers.
    """
    def __init__(self):
        if self.__class__ == PropbankPoitner:
            raise NotImplementedError()

class PropbankChainTreePointer(PropbankPointer):
    def __init__(self, pieces):
        self.pieces = pieces
        """A list of the pieces that make up this chain.  Elements may
           be either ``PropbankSplitTreePointer`` or
           ``PropbankTreePointer`` pointers."""

    def __str__(self):
        return '*'.join('%s' % p for p in self.pieces)
    def __repr__(self):
        return '<PropbankChainTreePointer: %s>' % self
    def select(self, tree):
        if tree is None: raise ValueError('Parse tree not avaialable')
        return Tree('*CHAIN*', [p.select(tree) for p in self.pieces])

class PropbankSplitTreePointer(PropbankPointer):
    def __init__(self, pieces):
        self.pieces = pieces
        """A list of the pieces that make up this chain.  Elements are
           all ``PropbankTreePointer`` pointers."""

    def __str__(self):
        return ','.join('%s' % p for p in self.pieces)
    def __repr__(self):
        return '<PropbankSplitTreePointer: %s>' % self
    def select(self, tree):
        if tree is None: raise ValueError('Parse tree not avaialable')
        return Tree('*SPLIT*', [p.select(tree) for p in self.pieces])

class PropbankTreePointer(PropbankPointer):
    """
    wordnum:height*wordnum:height*...
    wordnum:height,

    """
    def __init__(self, wordnum, height):
        self.wordnum = wordnum
        self.height = height

    @staticmethod
    def parse(s):
        # Deal with chains (xx*yy*zz)
        pieces = s.split('*')
        if len(pieces) > 1:
            return PropbankChainTreePointer([PropbankTreePointer.parse(elt)
                                              for elt in pieces])

        # Deal with split args (xx,yy,zz)
        pieces = s.split(',')
        if len(pieces) > 1:
            return PropbankSplitTreePointer([PropbankTreePointer.parse(elt)
                                             for elt in pieces])

        # Deal with normal pointers.
        pieces = s.split(':')
        if len(pieces) != 2: raise ValueError('bad propbank pointer %r' % s)
        return PropbankTreePointer(int(pieces[0]), int(pieces[1]))

    def __str__(self):
        return '%s:%s' % (self.wordnum, self.height)

    def __repr__(self):
        return 'PropbankTreePointer(%d, %d)' % (self.wordnum, self.height)

    def __cmp__(self, other):
        while isinstance(other, (PropbankChainTreePointer,
                                 PropbankSplitTreePointer)):
            other = other.pieces[0]

        if not isinstance(other, PropbankTreePointer):
            return cmp(id(self), id(other))

        return cmp( (self.wordnum, -self.height),
                    (other.wordnum, -other.height) )

    def select(self, tree):
        if tree is None: raise ValueError('Parse tree not avaialable')
        return tree[self.treepos(tree)]

    def treepos(self, tree):
        """
        Convert this pointer to a standard 'tree position' pointer,
        given that it points to the given tree.
        """
        if tree is None: raise ValueError('Parse tree not avaialable')
        stack = [tree]
        treepos = []

        wordnum = 0
        while True:
            #print treepos
            #print stack[-1]
            # tree node:
            if isinstance(stack[-1], Tree):
                # Select the next child.
                if len(treepos) < len(stack):
                    treepos.append(0)
                else:
                    treepos[-1] += 1
                # Update the stack.
                if treepos[-1] < len(stack[-1]):
                    stack.append(stack[-1][treepos[-1]])
                else:
                    # End of node's child list: pop up a level.
                    stack.pop()
                    treepos.pop()
            # word node:
            else:
                if wordnum == self.wordnum:
                    return tuple(treepos[:len(treepos)-self.height-1])
                else:
                    wordnum += 1
                    stack.pop()

class PropbankInflection(object):
    #{ Inflection Form
    INFINITIVE = 'i'
    GERUND = 'g'
    PARTICIPLE = 'p'
    FINITE = 'v'
    #{ Inflection Tense
    FUTURE = 'f'
    PAST = 'p'
    PRESENT = 'n'
    #{ Inflection Aspect
    PERFECT = 'p'
    PROGRESSIVE = 'o'
    PERFECT_AND_PROGRESSIVE = 'b'
    #{ Inflection Person
    THIRD_PERSON = '3'
    #{ Inflection Voice
    ACTIVE = 'a'
    PASSIVE = 'p'
    #{ Inflection
    NONE = '-'
    #}

    def __init__(self, form='-', tense='-', aspect='-', person='-', voice='-'):
        self.form = form
        self.tense = tense
        self.aspect = aspect
        self.person = person
        self.voice = voice

    def __str__(self):
        return self.form+self.tense+self.aspect+self.person+self.voice

    def __repr__(self):
        return '<PropbankInflection: %s>' % self

    _VALIDATE = re.compile(r'[igpv\-][fpn\-][pob\-][3\-][ap\-]$')

    @staticmethod
    def parse(s):
        if not isinstance(s, basestring):
            raise TypeError('expected a string')
        if (len(s) != 5 or
            not PropbankInflection._VALIDATE.match(s)):
            raise ValueError('Bad propbank inflection string %r' % s)
        return PropbankInflection(*s)
