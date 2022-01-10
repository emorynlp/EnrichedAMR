from prepare import *


def find_agentive_nouns(triple_find, g):
    '''Find the correct alignment for agentive/patient nouns'''
    if re.match(r'.*-[0-9]+', triple_find[2]):  # check if the plural alignment is a predicate
        trip_arg = [trip for trip in g.triples if
                    trip[0] == triple_find[0] and re.match(r':ARG[0-9]', trip[1])]  # find the arguments of the predicate
        if trip_arg:
            for t in trip_arg:
                trip_person = [trip for trip in g.triples if
                               trip[2] in ['person', 'thing', 'product', 'government-organization', 'organization'] and trip[0] == t[2]]  # check if the triple is (p / person)
                # aln_t = make_alignment(g, t)
                if trip_person:
                    triple_find = trip_person[0]  # change the plural triple to (p / person) if its a agentive noun
    return triple_find


def find_have_role(triple_find, g):
    '''Find the correct alignment for relational and organizational nouns'''
    # have-rel/org-role-91
    parent = [trip for trip in g.triples if
              trip[2] == triple_find[0] and re.match(r':ARG[0-9]', trip[1])]  # find the parent of the plural triple
    if parent:
        parent_inst = [trip for trip in g.triples
                       if trip[0] == parent[0][0] and trip[2] in ['have-rel-role-91', 'have-org-role-91']]  # check if the triple instance is have-rel/org-role
        parent_temp = [trip for trip in g.triples
                       if trip[0] == parent[0][0] and trip[2] in ['date-entity']]
        if parent_temp:
            triple_find = parent_temp[0]     # for date-entity
        if parent_inst:
            trip_arg = [trip for trip in g.triples if
                        trip[0] == parent_inst[0][0] and trip[1] == ':ARG0']  # find the argument0 of the predicate
            if trip_arg:
                trip_person = [trip for trip in g.triples if
                               trip[2] in ['person', 'organization'] and trip[0] == trip_arg[0][2]]  # check if the triple is (p / person)
            if trip_person:
                triple_find = trip_person[0]  # change the plural triple to (p / person) if its in have-rel/org-role-91
    return triple_find


def is_unit(triple, g):
    '''check if the triple has a unit role'''
    parent = [trip for trip in g.triples if
              trip[2] == triple[0] and re.match(r':unit', trip[1])]  # find the parent of the plural triple
    if parent:
        return True
    else:
        return False


def is_attribute(triple, g):
    '''check if the triple takes an attribute'''
    if "\"" in triple[2]:
        return True
    else:
        return False


def is_instance(triple, g):
    '''check if the triple is an instance'''
    if triple[1]==':instance':
        return True
    else:
        return False
