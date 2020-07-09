#Author: Toms Bergmanis toms.bergmanis@gmail.com
import os
import sys
import glob
path_to_treebanks=sys.argv[1]
langs = sys.argv[2:]

files = [("ud-dev.conllu", "dev"), ("ud-test.conllu", "test"), ("ud-train.conllu", "train")]

for lang in langs:
    for file_name, file_type in files:
        data = []
        
        udt_source_file = glob.glob('{}/UD_{}/*-{}'.format(path_to_treebanks,lang,file_name))[0]
        with open(udt_source_file, "r") as f:
            sentence = []
            for line in f:
                lc = line.strip().split()
                if len(lc) < 2:
                    continue
                elif lc[0] == "#":
                    continue
                elif lc[0].isdigit():
                    if int(lc[0]) == 1:
                        for i, (inflection, lemma, POS, tags) in enumerate(sentence):
                            out = " <s> ".join([" ".join(l for l in inflection) if i != j else "<SURFACE_FORM>" for j, (inflection, lemma, POS, tags) in enumerate(sentence)])
                            data.append((inflection, lemma, POS, out, tags))
                        sentence = []
                    POS = lc[3]
                    if POS == "PUNCT":
                        continue
                    inflection = lc[1]
                    lemma = lc[2]
                    if lemma == "": 
                        continue
                    if any([True if d in inflection+lemma else False for d in "+.,/1234567890-"]):
                        continue
                    tags = lc[5]
                    sentence.append((inflection, lemma, POS, tags))

        with open("{}/UD_{}/{}".format(path_to_treebanks, lang, file_type), "w") as f:
            for inflection, lemma, POS, out, tags in data:
                if lemma != "":
                    f.write("{}\t{}\t{}\t{}\t{}\n".format(inflection, lemma, POS, out, tags))
                    
