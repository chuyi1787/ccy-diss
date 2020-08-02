import os
import re

dataDir = "../data-bpe"


def readFile(fname):
    with open(fname, "r") as f:
        fc = f.read()
        fc = fc.split("\n")
    return fc


if __name__ == '__main__':
    for item in os.listdir(dataDir):
        if item[0] not in "ASET":
            continue
        print("process {}".format(item))
        typeDir = "{}/{}".format(dataDir, item)
        train_data = readFile("{}/train-sources".format(typeDir))

        # get all surface form in training data
        surface_form_list = []
        for i, line in enumerate(train_data):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos]
                surface_form = ''.join(subw for subw in surface_form.split()).lower()
                if surface_form not in surface_form_list:
                    surface_form_list.append(surface_form)
            except:
                pass

        dev_s = readFile("{}/dev-sources".format(typeDir))
        dev_t = readFile("{}/dev-targets".format(typeDir))
        s1 = open("{}/dev-unseen-sources".format(typeDir), "w")
        t1 = open("{}/dev-unseen-targets".format(typeDir), "w")
        for i, line in enumerate(dev_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos]
                surface_form = ''.join(subw for subw in surface_form.split())
                if surface_form.lower() not in surface_form_list:
                    s1.write("{}\n".format(line))
                    lemma = dev_t[i]
                    t1.write("{}\n".format(lemma))
            except:
                pass

        test_s = readFile("{}/test-sources".format(typeDir))
        test_t = readFile("{}/test-targets".format(typeDir))
        s2 = open("{}/test-unseen-sources".format(typeDir), "w")
        t2 = open("{}/test-unseen-targets".format(typeDir), "w")
        for i, line in enumerate(test_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos]
                surface_form = ''.join(subw for subw in surface_form.split())
                if surface_form.lower() not in surface_form_list:
                    s2.write("{}\n".format(line))
                    lemma = test_t[i]
                    t2.write("{}\n".format(lemma))
            except:
                pass




