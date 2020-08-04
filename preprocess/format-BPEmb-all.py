import sys
from collections import defaultdict
import bpemb
import re
import random

# flag=0
fname = sys.argv[1]  #e.g., selectedUDT-v2.1/UD_English/dev or test or train
lang = sys.argv[2]  #English ##source language type
ftype = sys.argv[3]  #e.g., dev  ## wich text
merge_N = int(sys.argv[4]) #500
context_N = int(sys.argv[5]) #N-char context
try:
    nk_tokens = int(sys.argv[6])
except:
    nk_tokens = 9999
    # flag = 1


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

                surface_form = encoder.encode(surface_form)
                surface_form = " ".join(x for x in surface_form)
                surface_form = surface_form.replace("▁", "")

                a = "{} {} {} {} {} {} {}\n".format(WBEGIN, lc_out, LC, surface_form, RC, rc_out, WEND)
                s.write(a)
                # write {}-tragets doc
                t.write("{} {} {}\n".format(WBEGIN, " ".join([l for l in lemma]), WEND))


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


if __name__ == '__main__':
    data = readFile(fname)
    surface_form2lemma = defaultdict(list)
    surface_form2sent = defaultdict(list)
    selected_dno = []

    # if flag == 0:
    #     m = nk_tokens * 1000
    #     total_examples = range(len(data))
    #     selected_dno = random.sample(total_examples, m)

    count = 0
    for i, line in enumerate(data):
        try:
            lc = line.split("\t")
            surface_form = lc[0]
            lemma = lc[1]
            POS = lc[2]
            sentence = lc[3]
            if lemma == "":
                continue
            # omit examples whose lemma contain "0987654321-/"
            if any([True if d in lemma else False for d in "0987654321-/"]):
                continue

            if count < (nk_tokens*1000):
                surface_form2lemma[surface_form].append(lemma)
                surface_form2sent[surface_form].append((sentence, lemma))
                count += 1
            else:
                break
            # if flag:
            #     surface_form2lemma[surface_form].append(lemma)
            #     surface_form2sent[surface_form].append((sentence, lemma))
            # else:
            #     if i in selected_dno:
            #         surface_form2lemma[surface_form].append(lemma)
            #         surface_form2sent[surface_form].append((sentence, lemma))
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

