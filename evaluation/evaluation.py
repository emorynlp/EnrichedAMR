import penman
import re


def count_f1(anno1, anno2, dict):
    '''count the number of tp, fp, fn occurances and store them in a dictionary'''
    # tp: Items classified by 2 which were classified by 1
    for x in anno2:
        if x in anno1:
            dict['tp'] += 1

    # fp: Items classified by 2 which were not classified by 1
    for x in anno2:
        if not (x in anno1):
            dict['fp'] += 1

    # fn: Items classified by 1 which were missed by 2
    for x in anno1:
        if not (x in anno2):
            dict['fn'] += 1


# Precision, Recall, F1 for annotator1 as standard
def f1(dict):
    '''calculate the f1 score'''
    tp = dict['tp']
    fp = dict['fp']
    fn = dict['fn']
    if tp + fp == 0:
        return "No tp+fp"
    elif tp + fn == 0:
        return "No tp+fn"
    precision = tp / (tp + fp)
    print(tp, fp, precision)
    recall = tp / (tp + fn)
    print(tp, fn, recall)
    if precision + recall == 0:
        return None
    else:
        return 2 * ((precision * recall) / (precision + recall))


def get_plural(g):
    '''returns all the plural occurances in the graph'''
    inst = []
    for trip in g.triples:
        if trip[1] == ':instance' and re.match(r'.*\.pl', trip[2]):
            inst.append(trip)
    return inst


def get_article(g):
    '''returns all the article occurances in the graph'''
    inst = []
    for trip in g.triples:
        if trip[1] == ':def':
            parent = [x for x in g.triples if x[0]==trip[0] and x[1]==':instance']
            if len(parent) > 0:
                name = parent[0][2][:-3] if re.search('.*\.pl', parent[0][2]) else parent[0][2]
                inst.append((name, trip[2]))
    return inst


def get_quantifier(g):
    '''returns all the quantifier occurances in the graph'''
    inst = []
    for trip in g.triples:
        if trip[2] in ['all', 'every', 'some', 'each', 'none']:
            parent = [x for x in g.triples if x[0]==trip[0] and x[1]==':instance']
            if len(parent) > 0:
                inst.append((parent[0][2], trip[2]))
    return inst


def get_content(g):
    '''returns all the :content occurances in the graph'''
    inst = []
    for trip in g.triples:
        if trip[1] == ':content':
            parent = [x for x in g.triples if x[0] == trip[0] and x[1] == ':instance']
            child = [x for x in g.triples if x[0] == trip[2] and x[1] == ':instance']
            if len(parent) > 0 and len(child) > 0:
                parent_name = parent[0][2][:-3] if re.search('.*\.pl', parent[0][2]) else parent[0][2]
                child_name = child[0][2][:-3] if re.search('.*\.pl', child[0][2]) else child[0][2]
                inst.append((parent_name, child_name))
    return inst


def evaluation(filename1, filename2):

    with open(filename1) as raw:
        data1 = raw.read()

    with open(filename2) as raw:
        data2 = raw.read()

    amrs1 = penman.iterparse(data1)
    amrs2 = penman.iterparse(data2)

    tasks = ['Plural', 'Article', 'Quantifier', 'Intensionality', 'Overall']
    dict = {task:{'tp': 0, 'fp': 0, 'fn': 0, 'f1': 0} for task in tasks}

    for amr1, amr2 in zip(amrs1, amrs2):
        g1 = penman.layout.interpret(amr1, model=None)
        g2 = penman.layout.interpret(amr2, model=None)

        count_f1(get_plural(g1), get_plural(g2), dict['Plural'])
        count_f1(get_article(g1), get_article(g2), dict['Article'])
        count_f1(get_quantifier(g1), get_quantifier(g2), dict['Quantifier'])
        count_f1(get_content(g1), get_content(g2), dict['Intensionality'])

    for key in dict['Overall'].keys():
        dict['Overall'][key] = dict['Plural'][key] + dict['Article'][key] + dict['Quantifier'][key] + dict['Intensionality'][key]

    dict['Plural']['f1'], dict['Article']['f1'], dict['Quantifier']['f1'], dict['Intensionality']['f1'], dict['Overall']['f1'] = f1(dict['Plural']), f1(dict['Article']), f1(dict['Quantifier']), f1(dict['Intensionality']), f1(dict['Overall'])

    return dict

