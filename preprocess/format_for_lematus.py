#Author: Toms Bergmanis toms.bergmanis@gmail.com
import sys
from collections import defaultdict

fname = sys.argv[1]
lang = sys.argv[2]
ftype = sys.argv[3]
try:
    n = int(sys.argv[4])
except:
    n = 20

WBEGIN = '<w>'
WEND = '</w>'

LC = '<lc>'
RC = '<rc>'

def readFile(fname):
    with open(fname, "r") as f:
        fc = f.read()
        fc = fc.split("\n")
    return fc

def write_data_to_files(data, fName):
    with open(fName + '-sources', "w") as s:
        with open(fName + '-targets', "w") as t:
            for context, surface_form, lemma, in data:
                s.write("{} {} {}\n".format(WBEGIN, trim_input(context, n, " ".join([l for l in surface_form])), WEND))
                t.write("{} {} {}\n".format(WBEGIN, " ".join([l for l in lemma]), WEND))

def trim_input(inp, n, surface_form):
    if n > 0:
        cs = inp.split("<SURFACE_FORM>")
        lc = cs[0].split(" ")
        lc = " ".join(lc[-min(n, len(lc)):])
        rc = cs[1].split(" ")
        rc = " ".join(rc[:min(n, len(rc))])
        return "{} {} {} {} {}".format(lc, LC, surface_form, RC, rc)
    else:
        return "{} {} {} {} {}".format( LC, surface_form, RC)

data = readFile(fname)

surface_form2lemma = defaultdict(list)
surface_form2sent = defaultdict(list)

for line in data:
    try:
        lc =  line.split("\t")
        surface_form = lc[0]
        lemma = lc[1]
        POS = lc[2]
        sentence = lc[3]
        if lemma == "": 
            continue
        if any([True if d in lemma else False for d in "0987654321-/"]):
            continue
        surface_form2lemma[surface_form].append(lemma)
        surface_form2sent[surface_form].append((sentence, lemma))
    except:
        pass

data = []
for surface_form, lemmas in surface_form2lemma.items():
    for sentence, lemma in surface_form2sent[surface_form]:
       data.append((sentence, surface_form, lemma)) 

write_data_to_files(data, "{}".format(ftype))

