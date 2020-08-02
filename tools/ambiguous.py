import os
import re
import sys

aaa=sys.argv[1] #data-char
dataDir = "../{}".format(aaa)


def readFile(fname):
    with open(fname, "r") as f:
        fc = f.read()
        fc = fc.split("\n")
    return fc


def get_ambiguous_wList(train_s, train_t):
    surface_form_collection = {}
    ambiguous_wlist = []
    ambiguous_dic = {}
    count = 0
    for i, line in enumerate(train_s):
        try:
            lPos = re.search("<lc>", line).span()[1]
            rPos = re.search("<rc>", line).span()[0]
            surface_form = line[lPos:rPos]
            surface_form = ''.join(subw for subw in surface_form.split()).lower()
            lemma = train_t[i].lower()
            if surface_form not in surface_form_collection:  # new type
                surface_form_collection[surface_form] = [lemma]
            else:
                if lemma not in surface_form_collection[surface_form]:  # ambiguous
                    count += 1
                    surface_form_collection[surface_form].append(lemma)
                    if surface_form not in ambiguous_wlist:  # add to ambiguous_wlist
                        ambiguous_wlist.append(surface_form)
                        ambiguous_dic[surface_form] = surface_form_collection[surface_form]
        except:
            pass

    print("ambiguous types in train data: {}".format(len(ambiguous_wlist)))
    print("ambiguous tokens in train data: {}".format(count))
    return ambiguous_wlist


if __name__ == '__main__':
    for item in os.listdir(dataDir):
        if item[0] not in "ASET":
            continue
        typeDir = "{}/{}".format(dataDir, item)
        print("++++++++process {}".format(typeDir))

        train_s = readFile("{}/train-sources".format(typeDir))
        train_t = readFile("{}/train-targets".format(typeDir))
        ambiguous_wlist = get_ambiguous_wList(train_s, train_t)  # all words are at low case


        dev_s = readFile("{}/dev-sources".format(typeDir))
        dev_t = readFile("{}/dev-targets".format(typeDir))
        s1 = open("{}/dev-ambiguous-sources".format(typeDir), "w")
        t1 = open("{}/dev-ambiguous-targets".format(typeDir), "w")
        count = 0
        amb_token_dev = []
        for i, line in enumerate(dev_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos]
                surface_form = ''.join(subw for subw in surface_form.split())
                if surface_form.lower() in ambiguous_wlist:  # this type is ambiguous
                    count += 1
                    s1.write("{}\n".format(line))
                    lemma = dev_t[i]
                    t1.write("{}\n".format(lemma))
                    if surface_form.lower() not in amb_token_dev:
                        amb_token_dev.append(surface_form.lower())
                    # if surface_form != surface_form.lower():
                    #     print(surface_form, lemma)
            except:
                pass

        print("ambiguous types in dev data: {}".format(len(amb_token_dev)))
        print("ambiguous tokens in dev data: {}".format(count))
