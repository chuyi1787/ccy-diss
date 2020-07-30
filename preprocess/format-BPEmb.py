import sys
from collections import defaultdict
import bpemb
import re
import random

fname = sys.argv[1]  #e.g., selectedUDT-v2.1/UD_English/dev or test or train
lang = sys.argv[2]  #English ##source language type
ftype = sys.argv[3]  #e.g., dev  ## wich text
merge_N = int(sys.argv[4]) #500
context_N = int(sys.argv[5]) #N-char context
try:
    nk_tokens = int(sys.argv[6])
except:
    nk_tokens = 9999


# lang = "English"
# fname = "selectedUDT-v2.1/UD_{}/train".format(lang)
# ftype = "train"
# merge_N = 500  # vocabulary size
# context_N = 20
# nk_tokens = 10


L_BPEmb = ""
if lang=="English":
    L_BPEmb = "en"
elif lang=="Spanish":
    L_BPEmb = "es"
elif lang=="Turkish":
    L_BPEmb = "tr"
elif lang=="Arabic":
    L_BPEmb = "ar"
else:
    print("language type error!!!!!!!!")



WBEGIN = '<w>'
WEND = '</w>'

LC = '<lc>'
RC = '<rc>'


def readFile(fname):
    with open(fname, "r") as f:
        fc = f.read()
        fc = fc.split("\n")
    return fc


# input is list of tuples: [(sentence, surface_form, lemma)]
# output is source and target file
def write_data_to_files(data, fName):
    with open(fName + '-sources', "w") as s:
        with open(fName + '-targets', "w") as t:
            for context, surface_form, lemma, in data:
                a = trim_input(context, context_N, " ".join([l for l in surface_form]))
                s.write("{} {} {}\n".format(WBEGIN, trim_input(context, context_N, " ".join([l for l in surface_form])), WEND))
                t.write("{} {} {}\n".format(WBEGIN, " ".join([l for l in lemma]), WEND))


def write_data_to_files_bpe(data, fName, encoder):
    with open(fName + '-sources', "w") as s:
        with open(fName + '-targets', "w") as t:
            for context, surface_form, lemma, in data:
                cs = context.split("<SURFACE_FORM>")
                lc = cs[0].split(" ")
                lc = " ".join(lc[-min(context_N, len(lc)):])
                w_list = chas2w(lc)
                lc_out = encoder.encode(" ".join(w for w in w_list))
                lc_out = " ".join(x for x in lc_out)
                lc_out = lc_out.replace("▁", "< ").replace("<", "<s>")

                rc = cs[1].split(" ")
                rc = " ".join(rc[:min(context_N, len(rc))])
                w_list = chas2w(rc)
                rc_out = encoder.encode(" ".join(w for w in w_list))
                rc_out = " ".join(x for x in rc_out)
                rc_out = rc_out.replace("▁", "< ").replace("<", "<s>")
                surface_form = " ".join(re.compile('.{1}').findall(surface_form))

                a = "{} {} {} {} {} {} {}\n".format(WBEGIN, lc_out, LC, surface_form, RC, rc_out, WEND)
                s.write(a)
                # write {}-tragets doc
                t.write("{} {} {}\n".format(WBEGIN, " ".join([l for l in lemma]), WEND))


# inp example: '<SURFACE_FORM> <s> t h e <s> A P <s> c o m e s <s> t h i s <s> s t o r y'
# output example: ' <lc> F r o m <rc>  <s> t h e <s> A P <s> c o m e s <s> t h i s <s>'
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


def chas2w(sent):
    sent = re.split("<s>", sent)
    w_list = []
    for w in sent:
        w = w.strip()
        if len(w) == 0:
            continue
        w = ''.join(c for c in w.split())
        w_list.append(w)
    return w_list


# prepare corpus for fit bpe
def bpe_cp_pp(sent, corpus_for_bpe, direct='b'):
    sent = re.split("<w>|</w>|<s>|<lc>|<rc>", sent)
    sent_ctn = ['<w>']
    for w in sent:
        w = w.strip()
        if len(w) == 0:
            continue
        w = ''.join(c for c in w.split())
        sent_ctn.append(w)
    sent_ctn = ' '.join(w for w in sent_ctn)
    sent_ctn += ' </w>'
    corpus_for_bpe.append(sent_ctn)
    return corpus_for_bpe


if __name__ == '__main__':
    data = readFile(fname)
    surface_form2lemma = defaultdict(list)
    surface_form2sent = defaultdict(list)

    m = nk_tokens * 1000
    total_examples = range(len(data))
    selected_dno = random.sample(total_examples, m)

    for i, line in enumerate(data):
        try:
            lc = line.split("\t")
            surface_form = lc[0]
            lemma = lc[1]
            POS = lc[2]
            sentence = lc[3]
            if lemma == "":
                continue
            if any([True if d in lemma else False for d in "0987654321-/"]):
                continue
            if i in selected_dno:
                surface_form2lemma[surface_form].append(lemma)
                surface_form2sent[surface_form].append((sentence, lemma))
        except:
            pass

    data = []
    surface_form_list = []
    for surface_form, lemmas in surface_form2lemma.items():
        if surface_form not in surface_form_list:
           surface_form_list.append(surface_form)
        for sentence, lemma in surface_form2sent[surface_form]:
           data.append((sentence, surface_form, lemma))


    encoder = bpemb.BPEmb(lang=L_BPEmb, vs=merge_N)
    write_data_to_files_bpe(data, "{}".format(ftype), encoder)


