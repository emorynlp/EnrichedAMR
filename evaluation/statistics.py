import penman
import re


def count_changes(g, count):
    for trip in g.triples:
        if trip[1] == ':instance' and re.match(r'.*\.pl', trip[2]):
            count['plural'] += 1
        if trip[1] == ':def' and trip[2] in ['+', '-']:
            count['article'] += 1
        if trip[1] == ':content':
            count['content'] += 1
        if trip[2] in ['all', 'every', 'some', 'each', 'none'] and trip[1] == ':quant':
            count['quantifier'] += 1


def statistics(filename):
    with open(filename) as raw:
        data = raw.read()

    amrs = penman.iterparse(data)
    count = {'plural': 0, 'article': 0, 'quantifier': 0, 'content': 0}

    for amr in amrs:
        g = penman.layout.interpret(amr, model=None)
        count_changes(g, count)

    return count
