import sys
languages = sys.argv[1]  # "Turkish"
type = sys.argv[2]  #"20-char-context"
model_n = sys.argv[3]

name = "{}-{}".format(languages,type)
reference = "data/{}/test-targets".format(name)
prediction = "models/{}/{}_step_{}_pred.txt".format(name, name, model_n)

ref = open(reference, "r").read().split("\n")
pred = open(prediction, "r").read().split("\n")
i = 0
j = 0
for line in pred:
    line = line.strip()
    if ref[i] == line:
        j += 1
    i+=1
print(float(j)/i)
