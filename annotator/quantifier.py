from prepare import *
from cornerCases import *

quantifiers = ['all', 'every', 'some', 'each', 'none']
gen_quants = ['everybody', 'everyone', 'everything', 'somebody', 'someone', 'something', 'nobody', 'no-one', 'nothing']


def convert_quant(g):
    gen_quant(g)
    mod_to_quant(g)


def mod_to_quant(g):
    '''convert quantifiers with :quant or :mod role to attributes'''
    try:
        delete = []
        for i in range(len(g.triples)):
            if g.triples[i][2] in quantifiers:
                child = [item for item in g.triples if item[0]==g.triples[i][0]]
                if len(child) > 1:  # leave cases that have children, signifies bad annotation
                    continue
                parent = [item for item in g.triples if item[2]==g.triples[i][0]]
                if len(parent) > 0:
                    if parent[0][1] not in [':mod', ':quant']:  # check only quantifiers that takes :mod and :quant role
                        continue
                    # deal with multiple :quant roles under one parent
                    siblings = [item for item in g.triples if item[0]==parent[0][0] and item[1] in [':quant', ':mod'] and item[2] != g.triples[i][0]]
                    conflict = False
                    for sib in siblings:
                        other_quant = [item for item in g.triples if
                                                item[0] == sib[2] and item[2] in quantifiers]
                        if sib[2] in quantifiers:
                            conflict = True
                        elif len(other_quant) > 0:
                            ind_other_quant = [index for index in range(len(g.triples)) if g.triples[index] == other_quant[0]][0]
                            ind = [index for index in range(len(g.triples)) if g.triples[index] == sib][0]
                            delete.append(g.triples[ind])
                            delete.append(g.triples[ind_other_quant])
                            conflict = True
                    if conflict:
                        continue

                align = make_alignment(g, g.triples[i])
                quant_trip = [item for item in g.triples if item[2] == g.triples[i][0]]
                for trip in quant_trip:
                    ind = [index for index in range(len(g.triples)) if g.triples[index] == trip][0]
                    # new = (g.triples[ind][0], ':quant', g.triples[i][2] + align)
                    new = (g.triples[ind][0], ':quant', g.triples[i][2])
                    g.triples.append(new)
                    delete.append(g.triples[ind])
                    delete.append(g.triples[i])
        for d in delete:
            g.triples.remove(d)
    except Exception as e:
        print("An error has occured for mod_to_quant:", e)
        pass



def gen_quant(g):
    try:
        gen_triples = [t for t in g.triples if t[2] in gen_quants]
        quants = ['every', 'some', 'no']
        for triple in gen_triples:
            align = make_alignment(g, triple)
            for quantifier in quants:
                if quantifier in triple[2]:
                    if 'body' in triple[2] or 'one' in triple[2]:
                        new_triple = (triple[0], triple[1], 'person'+align)
                    elif 'thing' in triple[2]:
                        new_triple = (triple[0], triple[1], 'thing'+align)
                    if quantifier=='no':
                        quantifier = 'none'
                    quant_triple = (triple[0], ':quant', quantifier+align)
            g.triples.append(new_triple)
            g.triples.append(quant_triple)
            g.triples.remove(triple)
    except Exception as e:
        print("An error has occured for gen_quant:", e)
        pass


