import os
import re
import string
import sys

print(string.punctuation)

dataName = sys.argv[1]  # data-char
dataDir = "../data/{}".format(dataName)


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


if __name__ == '__main__':
    for item in os.listdir(dataDir):
        if item[0] not in "ASET":
            continue
        print("+++++++++process {}".format(item))
        typeDir = "{}/{}".format(dataDir, item)
        train_data = readFile("{}/train-sources".format(typeDir))

        # get all surface form (standardized in lower case) in training data
        # print("Get all surface_form from trainD:")
        surface_form_list = []
        for i, line in enumerate(train_data):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos].strip()
                surface_form = ''.join(subw for subw in surface_form.split()).lower()

                if CHECK(surface_form):  # invalid token
                    continue

                if surface_form not in surface_form_list:
                    surface_form_list.append(surface_form)
            except:
                pass
        print("total types in train: {}".format(len(surface_form_list)))
        print("total examples in train: {}".format(i))

        # print("begin write dev-unseen")
        dev_s = readFile("{}/dev-sources".format(typeDir))
        dev_t = readFile("{}/dev-targets".format(typeDir))
        s1 = open("{}/dev-unseen-sources".format(typeDir), "w")
        t1 = open("{}/dev-unseen-targets".format(typeDir), "w")
        surface_form_list_dev = []
        unseen_surface_form_list = []
        count = 0
        for i, line in enumerate(dev_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos].strip()
                surface_form = ''.join(subw for subw in surface_form.split()).lower()

                if surface_form not in surface_form_list_dev:
                    surface_form_list_dev.append(surface_form)

                if CHECK(surface_form):  # invalid token
                    continue
                if surface_form not in surface_form_list:
                    s1.write("{}\n".format(line))
                    lemma = dev_t[i]
                    t1.write("{}\n".format(lemma))

                    count += 1
                    if surface_form not in unseen_surface_form_list:
                        unseen_surface_form_list.append(surface_form)
            except:
                pass
        print("total examples in dev: {}".format(i))
        print("total types in dev: {}".format(len(surface_form_list_dev)))
        print("unseen examples in dev: {}".format(count))
        print("unseen types in dev: {}".format(len(unseen_surface_form_list)))


        # print("begin write test-unseen")
        test_s = readFile("{}/test-sources".format(typeDir))
        test_t = readFile("{}/test-targets".format(typeDir))
        s1 = open("{}/test-unseen-sources".format(typeDir), "w")
        t1 = open("{}/test-unseen-targets".format(typeDir), "w")
        surface_form_list_test = []
        unseen_surface_form_list = []
        count = 0
        for i, line in enumerate(test_s):
            try:
                lPos = re.search("<lc>", line).span()[1]
                rPos = re.search("<rc>", line).span()[0]
                surface_form = line[lPos:rPos].strip()
                surface_form = ''.join(subw for subw in surface_form.split()).lower()

                if surface_form not in surface_form_list_test:
                    surface_form_list_test.append(surface_form)

                if CHECK(surface_form):  # invalid token
                    continue
                if surface_form not in surface_form_list:
                    s1.write("{}\n".format(line))
                    lemma = test_t[i]
                    t1.write("{}\n".format(lemma))

                    count += 1
                    if surface_form not in unseen_surface_form_list:
                        unseen_surface_form_list.append(surface_form)
            except:
                pass
        print("total examples in test: {}".format(i))
        print("total types in test: {}".format(len(surface_form_list_test)))
        print("unseen examples in test: {}".format(count))
        print("unseen types in test: {}".format(len(unseen_surface_form_list)))

