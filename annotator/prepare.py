import pandas as pd
import penman
from penman import surface
from nltk.parse.corenlp import CoreNLPParser
from lemminflect import getLemma
import re

parser = CoreNLPParser(tagtype='pos')


def get_parsed(snt):
    '''Parse constituency tree'''
    return next(parser.raw_parse(snt, verbose=False))


def get_penman(snt):
    '''Encode PENMAN graphs'''
    return penman.decode(snt)


def get_pos(snt):
    '''Extract POS tags'''
    tokens = snt.split()
    return parser.tag(tokens)


def get_alignment(g):
    '''
    Extract alignment information in a dictionary
    :param g: Penman graph
    :return: dictionary with tokens as keys and alignments as values
    '''
    alignments = surface.alignments(g)
    aligns = {}
    for align in alignments.keys():
        nums = str(alignments[align])[3:].split(',')
        for value in nums:
            aligns[value] = align
    return aligns


def align_number(g, triple):
    '''get the alignment number of triple'''
    if triple in surface.alignments(g).keys():
        align = str(surface.alignments(g)[triple])[3:].split(',')
    else:
        align = None
    return align


def make_alignment(g, triple):
    '''Create alignment information'''
    return str(surface.alignments(g)[triple])


def get_treeLabels(tree, path):
    '''get the labels of the path to a tree node'''
    label = []
    for i in range(len(path)):
            label.append(tree[path[:i]].label())
    return label


def get_subtree(tree, path):
    '''get the subtree from the path'''
    subtree = tree
    for i in range(len(path)-1):
        subtree = subtree[path[i]]
    return subtree


def check_SBAR(tree, index):
    '''
    check if a verb (VP) is followed by a sentential complement
    :param tree: a dependency tree
    :param index: the index of the verb
    :return: BOOLEAN, True if it is followed by SBAR, False otherwise
    '''
    result = False
    path = tree.leaf_treeposition(index)[:-1]
    token = tree[tree.leaf_treeposition(index)[:-1]].leaves()[0]
    subtree = get_subtree(tree, path)
    min = index
    max = -1
    j = 0
    while token not in subtree[j].leaves():
        j += 1
    for i in range(j, len(subtree)):
        if subtree[i].label() in ['SBAR', 'S']:
            result = True
            max = min + len(subtree[i].leaves()) - 1
        else:
            min += len(subtree[i].leaves())
    return result, [min, max]


def check_NP(tree, index):
    '''
    check if a verb (VP) is followed by a NP
    :param tree: a dependency tree
    :param index: the index of the verb
    :return: BOOLEAN, True if it is followed by NP, False otherwise
    '''
    result = False
    path = tree.leaf_treeposition(index)[:-1]
    token = tree[tree.leaf_treeposition(index)[:-1]].leaves()[0]
    subtree = get_subtree(tree, path)
    j = 0
    while token not in subtree[j].leaves():
        j += 1
    for i in range(j, len(subtree)):
        if subtree[i].label() == 'NP':
            result = True
    return result


def node_depth(epidata):
    """
    Uses penman epidata to determine node depth
    Returns dictionary {triple : depth} for triple in epidata
    where depth = depth of first node in triple
    """
    depth = 0
    tree_depth = {}
    for triple in epidata:
        tree_depth[triple] = depth
        if epidata[triple]:
            for stack_op in epidata[triple]:
                if isinstance(stack_op, penman.layout.Push):
                    depth += 1
                elif isinstance(stack_op, penman.layout.Pop):
                    depth -= 1
    return tree_depth
