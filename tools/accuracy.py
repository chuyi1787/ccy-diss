import sys
reference = sys.argv[1]  # data-bpeall/Arabic-100-BPEmb-all-15-context/dev-targets
prediction = sys.argv[2]  # models-bpeall/Arabic-100-BPEmb-all-15-context/dev_pred.txt


# full match accracy, ignore word case
ref = open(reference, "r").read().split("\n")
pred = open(prediction, "r").read().split("\n")
i = 0
j = 0
for line in pred:
    line = line.strip()
    if ref[i].lower() == line.lower():
        j += 1
    i+=1
acc = (float(j)/i)*100
print("%.4f" % acc )
