from cornerCases import *


def add_plural(snt, g):
    try:
        pos = get_pos(snt)
        aligns = get_alignment(g)
        for i in range(len(pos)):
            if pos[i][1] in ['NNS', 'NPS']:
                triple_pl = aligns[str(i)] if str(i) in aligns.keys() else None
                # Corner cases
                if triple_pl is None:
                    continue
                elif is_unit(triple_pl, g):
                    continue
                elif is_attribute(triple_pl, g):
                    continue
                elif not is_instance(triple_pl, g):
                    continue
                align = make_alignment(g, triple_pl)
                triple_pl = find_agentive_nouns(triple_pl, g)
                triple_pl = find_have_role(triple_pl, g)
                # General case, add plural marker
                for j in range(len(g.triples)):
                    trip = g.triples[j]
                    if trip == triple_pl:
                        new_trip = tuple([trip[0], trip[1], (trip[2] + '.pl' + align)])
                        g.triples.append(new_trip)
                        del g.triples[j]
    except Exception as e:
        print("An error has occured for plural:", e)
        pass

