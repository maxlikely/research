# coding: utf-8
import nltk
import numpy as np
from utilities.buckwalter2unicode import transliterateString

class APBTree(nltk.tree.Tree):
    '''

    Subclassing NLTK's default tree structure. I think this is the right choice
    as we will be making a lot of method that are really more for trees.

    '''

    def print_arabic(self):
        '''
        Prints the arabic leaves of the tree as a nice sentence. Most of the
        code here is to clean up formatting.
        '''

        leaves = [x for x, y in self.pos() if y != '-NONE-']
        sentence = ' '.join(leaves)

        sentence = sentence.replace(' ?', u'\u2E2E')
        sentence = sentence.replace(' ,', u'\u060C')

        appenders = [u'\u0628',
                     u'\u0648',
                     u'\u0648',
                     u'\u0648']

        for appender in appenders:
            sentence = sentence.replace(appender + ' ', appender)

        return sentence

    def __str__(self):
        return self.pprint(margin=99999999999)

    def __repr__(self):
        return self.pprint(margin=99999999999)

    def lowest_common_ancestor(self, source, target):
        '''
        takes two tree positions, source and target, and returns
        their lowest common ancestor
        source = (2,2,0,0)
        target = (2,2,1,0,0,0,0)
        lowest_common_ancestor(source, target) := (2,2)

        returns () if no common ancestor
        '''

        i = 0
        min_length = min(len(source), len(target))
        while i < min_length and source[i] == target[i]:
            i += 1
        return source[:i]

    def collapse_sbar(self):
        '''
        Removes all SBAR nodes from parse tree. Assumes
        root is not SBAR.
        '''

        def collapse_sbar_recursive(tree):
            '''
            Helper function to do this recursively.
            '''

            # I'm a leaf, leaf me alone!
            if not isinstance(tree, APBTree):
                return tree

            # collapse all children
            children = []
            for child in tree:
                child = collapse_sbar_recursive(child)

                # check if I returned a list of trees or a tree
                if isinstance(child, APBTree) or isinstance(child, unicode) or isinstance(child, str):
                    children.append(child)
                else:
                    children.extend(child)

            if tree.node == 'SBAR':
                tree     = children
            else:
                tree[0:] = children

            return tree

        self = collapse_sbar_recursive(self)

    # FIXME: Seriously heuristic-tastic, FIX THIS, it doesn't do what it's
    # supposed to yet... currently it just grabs the last nodes of the
    # argument, really need to make it so we can replace all argument span with
    # a new node...
    def get_arg_node_position(self, arg_text):
        '''
        Returns the possible argument node for an argument. Note,
        this is completely heuristic, we need to clean this up.

        Could probably insert a new "arg node in tree and make its
        children all sub trees that span between the first and last.
        '''

        self.collapse_sbar()
        leaves = self.leaves()

        # check if the stupid argument has something like *T*-1 &lt; التوجه
        # if it does, we need to search for just *T*-1, if not, we should
        # disregard it from our searching of the leaves. This thing is so dumb,
        # I really wonder if we're using the proper dataset to do all these
        # hacks. For instance, we can't even search in the leaves because
        # clitics are separated as well...
        if '-NONE-' in arg_text:
            words = arg_text.split()[0]
        else:
            words = arg_text.split()

        first, last = words[0], words[-1]

        try:
            start = leaves.index(first)
            end   = leaves.index(last)
        except:
            dist  = nltk.metrics.distance.edit_distance
            start = np.argmin([dist(first, leaf) for leaf in leaves])
            end   = np.argmin([dist(last,  leaf) for leaf in leaves])

        # add a new child to lowest common ancestor, this child will have all
        # children between start and end
        #new_parent = self.treeposition_spanning_leaves(start, end)

        start = self.leaf_treeposition(start)
        end = self.leaf_treeposition(end)


        new_parent = self.lowest_common_ancestor(start, end)

        # TODO: finish this by inserting new node
        #new_parent.append(APBTree(argument, []))

        if start == end:
            return new_parent[:-1]
        else:
            return new_parent

        # was using for demo
        #return new_parent, self.leaf_treeposition(start), self.leaf_treeposition(end)

    def get_path(self, source, target):
        '''
        Finds a path between nodes in a tree
        '''
        a = len(self.lowest_common_ancestor(source, target))
        source_path = [(source[:x], u'\u2191') for x in xrange(len(source),a,-1)]
        target_path = [(target[:x], u'\u2193') for x in xrange(a,len(target))]
        path = source_path + target_path

        return path

    def get_predicate_supertree(self, predicate_node_position):
        '''
        Takes the tree position of the predicate node and returns a
        subtree rooted at the lowest S or SBAR node subsuming it.
        '''

        s_node = len(predicate_node_position)

        for s_node in xrange(len(predicate_node_position), 0, -1):
            if self[s_node].node == 'S' or self[s_node].node == 'SBAR':
                break

        return self[s_node]

    def get_predicate_node_position(self, predicate_text, pos):
        '''
        Returns the treeposition of a predicate node.
        '''

        def get_predicate_node(tree, predicate_text, pos):
            '''
            Retrieves the node in the tree that has the associated predicate (or any word)

            predicate: buckwalter representation of the arabic string
            pos: lowercase single character representing the predicate's part-of-speech
            tree: a parenthesis delimited string representation of the tree
            '''

            def replaceVowel(inputStr):
                # Replaces instances of these vowels in the input string
                for char in ['a', 'i', 'o']:
                    inputStr = inputStr.replace(char, '')
                return inputStr

            # POSs to filter search space
            if pos == 'n':
                predPosList = ['n', 'adj']
            else:
                predPosList = [pos]

            is_correct_pos = lambda item: any([tag in item[0][1].lower() for tag in predPosList])
            terminal_list  = filter(is_correct_pos, zip(tree.pos(), xrange(len(tree.pos()))))

            # Calculate the distance between each word and the predicate
            dist = nltk.metrics.distance.edit_distance

            words_and_idx = [(transliterateString(word, False), i) for (word,tag), i in terminal_list]
            scores = [dist(replaceVowel(predicate_text),
                            replaceVowel(word)) for word,i in words_and_idx]

            # Fetch the most likely predicateBranch
            predicate_node = words_and_idx[np.argmin(scores)][1]

            return predicate_node

        node = get_predicate_node(self, predicate_text, pos)
        return self.leaf_treeposition(node)[:-1] # do this to take the node, not terminal leaf
        #for position in self.treepositions():
        #    if node == self[position]:
        #        return position

        #return ()


def fix_parse_tree_text(tree_text, pos):# TODO: move this into the constructor for APBTree
    '''
    Fixes bugggy parse trees.
    '''

    # Get rid of random text before and after the tree
    openPI = tree_text.index('(')
    closePI = len(tree_text) - tree_text[::-1].index(')')

    tree_text = tree_text[openPI:closePI]

    # Enforce well-formedness of the bracketing
    openP = tree_text.count('(')
    closeP = tree_text.count(')')
    tree_text = ('(' * (closeP - openP)) + tree_text + (')' * (openP - closeP))
    tree_text = '(WTF ' + tree_text + ')'
    return tree_text


def clean_part_of_speech(tree):
    for child in tree:
        if isinstance(child, APBTree):
            child = clean_part_of_speech(child)
        else:
            tree.node = change_label(tree.node)
    return tree


def change_label(node):
    labels = ['NP', 'VP', 'PP', 'NOUN', 'PRON', 'VB', 'CONJ', 'PREP', 'PUNC', ]
    for label in labels:
        if label in node:
            return label
    return node

