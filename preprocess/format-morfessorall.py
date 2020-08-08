import sys
from collections import defaultdict
import morfessor
import re
io = morfessor.MorfessorIO()

fname = sys.argv[1]  #e.g., selectedUDT-v2.1/UD_English/dev or test or train
lang = sys.argv[2]  #English ##source language type
ftype = sys.argv[3]  #e.g., dev  ## wich text
context_N = int(sys.argv[4]) #N-char context
try:
    nk_tokens = int(sys.argv[5])
except:
    nk_tokens = 9999

# lang = "English"
# fname = "selectedUDT-v2.1/UD_{}/dev".format(lang)
# ftype = "dev"
# merge_N = 500  # vocabulary size
# context_N = 20
# nk_tokens = 10


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
def write_data_to_files(data, seg_model, fName):
    with open(fName + '-sources', "w") as s:
        with open(fName + '-targets', "w") as t:
            for context, surface_form, lemma, in data:
                cs = context.split("<SURFACE_FORM>")

                lc = cs[0].split(" ")
                lc = lc[-min(context_N, len(lc)):]  # ['<s>', 'a', 'p', 'p', '']
                lc_out = chas2segm(seg_model, lc, 'l')

                rc = cs[1].split(" ")
                rc = rc[:min(context_N, len(rc))]  # [ '', '<s>', 'a', 'p', 'p']
                rc_out = chas2segm(seg_model, rc, 'r')

                surface_form = " ".join(re.compile('.{1}').findall(surface_form))
                surface_form = chas2segm(seg_model, surface_form)

                a = "{} {} {} {} {} {} {}\n".format(WBEGIN, lc_out, LC, surface_form, RC, rc_out, WEND)
                s.write(a)
                t.write("{} {} {}\n".format(WBEGIN, " ".join([l for l in lemma]), WEND))


def chas2segm(seg_model, sent, direction='none'):
    sent_out_list = []

    # split sentence into word list, word are
    sent = " ".join(sent)
    sent = re.split("<s>", sent)

    for w in sent:  # w, e.g, " a p p "
        w = w.strip()
        w = ''.join(c for c in w.split())

        if len(w) == 0:
            continue
        else:
            segms = seg_model.viterbi_segment(w)
            sent_out_list.append(segms[0])

    sent_out = []
    for item in sent_out_list:
        item = " ".join(tri for tri in item)
        sent_out.append(item)
    sent_out = " <s> ".join(sent_out)

    if direction == 'l':
        sent_out = sent_out + " <s>"
    elif direction == 'r':
        sent_out = "<s> " + sent_out
    else:
        pass
    return sent_out


if __name__ == '__main__':
    data = readFile(fname)
    surface_form2lemma = defaultdict(list)
    surface_form2sent = defaultdict(list)

    count = 0
    for i, line in enumerate(data):
        try:
            lc = line.split("\t")
            surface_form = lc[0]
            lemma = lc[1]
            POS = lc[2]
            sentence = lc[3]
            # omit examples with empty lemma
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

        except:
            pass

    data = []
    surface_form_list = []
    for surface_form, lemmas in surface_form2lemma.items():
        if surface_form not in surface_form_list:
           surface_form_list.append(surface_form)
        for sentence, lemma in surface_form2sent[surface_form]:
           data.append((sentence, surface_form, lemma))

    seg_model = io.read_binary_model_file('morfessor-models/model-{}.segm.bi'.format(lang))

    write_data_to_files(data, seg_model, "{}".format(ftype))


