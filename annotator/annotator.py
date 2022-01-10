from content import *
from plural import *
from article import *
from quantifier import *


def convert(snt, g):
    add_article(snt, g)
    convert_quant(g)
    convert_content(snt, g)
    add_plural(snt, g)


def convert_corpus(input, output):
    '''
    Takes in a penman file name as the input file and a name for output file, and record the converted corpus in the output file
    '''

    with open(input) as raw:
        data = raw.read()

    amrs = penman.iterparse(data)
    tokens = re.findall('::snt.*', data)
    sents = [s[6:] for s in tokens]
    sents = [re.sub('@', '', s) for s in sents]
    text_file = open(output, 'w')

    for index, amr in enumerate(amrs):
        g = penman.layout.interpret(amr, model=None)
        snt = sents[index]
        convert(snt, g)
        text_file.write(penman.encode(g))
        text_file.write('\n\n')
