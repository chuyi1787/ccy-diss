dataDirName=$1 # data-char

echo "begin "${dataDirName}
python3 ambiguous.py ${dataDirName} >> data-situation/${dataDirName}.ambiguous
echo "finish"