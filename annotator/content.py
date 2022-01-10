from prepare import *



# Mega-veridicality verbs are extracted from the MegaVeridicality Project v1 (http://megaattitude.io/projects/mega-veridicality/)
# Reference: White, Aaron Steven, and Kyle Rawlins. 2018. The Role of Veridicality and Factivity in Clause Selection. In Proceedings of the 48th Annual Meeting of the North East Linguistic Society, edited by Sherry Hucklebridge and Max Nelson, 221–234. Amherst, MA: GLSA Publications.
attitude_verbs = list(pd.read_csv('verb-list2.csv')['0'])

intensional_trans_verbs = {'want-01': ':ARG1', 'expect-01': ':ARG1', 'need-01': ':ARG1', 'desire-01': ':ARG1', 'omit-01': ':ARG1',
                           'resemble-01': ':ARG2', 'imitate-01': ':ARG1', 'prefer-01': ':ARG1', 'imagine-01': ':ARG1', 'anticipate-01': ':ARG1','fear-01': ':ARG1'}
communication_verbs = ['say', 'tell', 'report']
modals = {'need-01': ':ARG1', 'possible-01': ':ARG1', 'obligate-01': ':ARG2', 'infer-01': ':ARG1', 'capable-01': ':ARG2', 'seem-01':':ARG1'}


def convert_content(snt, g):
    '''
    Convert the :ARG-X role to :content role for verbs used with intensional contexts
    '''
    try:
        tree = get_parsed(snt)
        triples = g.triples
        tokens = snt.split(" ")
        aligns = get_alignment(g)

        for i in range(len(tokens)):
            verb = getLemma(tokens[i], upos='VERB')[0]
            # check if exist in alignment
            if str(i) not in aligns.keys():
                # print("FAIL due to no alignment")
                continue
            else:
                triple_ver = aligns[str(i)]
            if verb in attitude_verbs:
                # Case 1: check if there is an intensional usage through sentential complement
                isSBAR, cont_range = check_SBAR(tree, i)
                if isSBAR:
                    # Find the appropriate argument role for intensional context
                    arg_roles = [item for item in triples if item[0] == triple_ver[0] and re.search(r":ARG[0-9]", item[1])] # all the :ARGX roles
                    arg_role = None # target arg role for change
                    if len(arg_roles) > 0:
                        for k in arg_roles:
                            arg_inst = [item for item in triples if item[0] == k[2] and item[1] == ':instance']
                            if len(arg_inst) == 0:
                                continue
                            else:
                                arg_inst = arg_inst[0]
                            if connectives(g, arg_inst, cont_range):
                                arg_role = k
                            inst_aln = align_number(g, arg_inst)
                            if inst_aln is None: continue
                            for x in inst_aln:
                                if int(x) >= cont_range[0] and int(x) <=cont_range[1]:
                                    arg_role = k
                        change_to_content(g, arg_role)
                # Case 2: frequently occured communicative verbs with inverted sentence structures
                elif verb in communication_verbs and not check_NP(tree, i):
                    arg1 = [item for item in triples if item[0] == triple_ver[0] and item[1] == ':ARG1']
                    if len(arg1) > 0:
                        change_to_content(g, arg1[0])


        for triple in triples:
            argX = []
            # Case 3: intensional transitive verbs
            if triple[2] in intensional_trans_verbs.keys():
                argX = [item for item in triples if item[0] == triple[0] and item[1] == intensional_trans_verbs[triple[2]]]
            # Case 4: AMR modals
            elif triple[2] in modals.keys():
                argX = [item for item in triples if item[0] == triple[0] and item[1] == modals[triple[2]]]
            if len(argX) > 0:
                change_to_content(g, argX[0])

    except Exception as e:
        print("An error has occured for content:", e)
        pass


def connectives(g, triple, cont_range):
    '''special treatment for connectives (and, or)'''
    is_content = False
    if triple[2] in ['and', 'or']:
        op_roles = [item for item in g.triples if item[0] == triple[0] and re.search(r":op[0-9]", item[1])]
        if len(op_roles) > 0:
            for op in op_roles:
                op_inst = [item for item in g.triples if item[0] == op[2] and item[1] == ':instance'][0]
                for x in align_number(g, op_inst):
                    if int(x) >= cont_range[0] and int(x) <= cont_range[1]:
                        is_content = True
    return is_content


def change_to_content(g, arg_role):
    '''convert content role'''
    triples = g.triples
    if arg_role is not None:
        for j in range(len(triples)):
            if triples[j] == arg_role:
                triples[j] = list(triples[j])
                triples[j][1] = ':content'
                triples[j] = tuple(triples[j])


