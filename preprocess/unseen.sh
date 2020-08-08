dataDirName=$1 # data-char

echo "begin "${dataDirName}
python3 unseen.py ${dataDirName} >> data-situation/${dataDirName}.unseen
echo "finish"
