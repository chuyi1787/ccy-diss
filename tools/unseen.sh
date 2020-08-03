dataDirName=$1 # data-char

echo "begin "${dataDirName}
python3 unseen.py ${dataDirName} >> ${dataDirName}.unseen
echo "finish"
