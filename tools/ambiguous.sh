dataDirName=$1 # data-char

echo "begin "${dataDirName}
python3 ambiguous.py ${dataDirName} >> ${dataDirName}.ambiguous
echo "finish"