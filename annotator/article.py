from cornerCases import *


def add_article(snt, g):
    try:
        pos = get_pos(snt)
        tree = get_parsed(snt)
        aligns = get_alignment(g)
        for i in range(len(pos)):
            if pos[i][1] == 'DT' and pos[i][0].lower() in ['the', 'a', 'an']:
                path = tree.leaf_treeposition(i)[:-1]
                subtree = get_subtree(tree, path)
                leaf = subtree.leaves()
                for k in range(len(leaf)):
                    noun = pos[i+k][0] if pos[i+k][1] in ['NN', 'NP', 'NNS', 'NPS', 'NNP'] else None
                    aln = i + k if pos[i+k][1] in ['NN', 'NP', 'NNS', 'NPS', 'NNP']  else None
                noun = pos[i+len(leaf)-1][0] if noun is None else noun
                aln = i+len(leaf)-1 if noun is None else aln
                triple_article = aligns[str(aln)] if str(aln) in aligns.keys() else None
                # Corner cases
                if triple_article is None:
                    continue
                elif is_attribute(triple_article, g):
                    continue
                elif not is_instance(triple_article, g):
                    continue
                elif is_unit(triple_article, g):
                    continue
                triple_article = find_agentive_nouns(triple_article, g)
                triple_article = find_have_role(triple_article, g)
                # General case, add article
                for j in range(len(g.triples)):
                    trip = g.triples[j]
                    align = "~e."+ str(i)
                    if trip == triple_article:
                        if pos[i][0].lower() in ['the']:
                            new_trip = tuple([trip[0], ':def', '+'])
                        else:
                            # new_trip = tuple([trip[0], ':def' + align, '-' + align])
                            new_trip = tuple([trip[0], ':def', '-'])
                        g.triples.append(new_trip)
    except Exception as e:
        print("An error has occured for article:", e)
        pass


