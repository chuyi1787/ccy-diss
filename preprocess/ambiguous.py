import os
import re
import sys
import string

aaa = sys.argv[1] #data-char
dataDir = "../data/{}".format(aaa)


def readFile(fname):
    with open(fname, "r") as f:
        fc = f.read()
        fc = fc.split("\n")
    return fc


# omit punctuation, tokens containing "@+._/0123456789"
def CHECK(surface_form):
    for c in surface_form:
        if c in "@+._/0123456789":
            # print(i, surface_form)
            return 1
    if surface_form in string.punctuation:
        # print(i, surface_form)
        return 1
    return 0


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

            if CHECK(surface_form):  # invalid token
                continue

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
    print("ambiguous examples in train data: {}".format(count))
    print("ambiguous types in train data: {}".format(len(ambiguous_wlist)))
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
        print("ambiguous examples in dev data: {}".format(count))
        print("ambiguous types in dev data: {}".format(len(amb_token_dev)))

        test_s = readFile("{}/test-sources".format(typeDir))
        test_t = readFile("{}/test-targets".format(typeDir))
        s2 = open("{}/test-ambiguous-sources".format(typeDir), "w")
        t2 = open("{}/test-ambiguous-targets".format(typeDir), "w")
        count = 0
        amb_token_test = []
        for i, line in enumerate(test_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos]
                surface_form = ''.join(subw for subw in surface_form.split())
                if surface_form.lower() in ambiguous_wlist:  # this type is ambiguous
                    count += 1
                    s2.write("{}\n".format(line))
                    lemma = test_t[i]
                    t2.write("{}\n".format(lemma))
                    if surface_form.lower() not in amb_token_test:
                        amb_token_test.append(surface_form.lower())
                    # if surface_form != surface_form.lower():
                    #     print(surface_form, lemma)
            except:
                pass
        print("ambiguous examples in test data: {}".format(count))
        print("ambiguous types in test data: {}".format(len(amb_token_test)))



