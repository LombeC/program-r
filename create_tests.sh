FILES=./bots/Ryan/aiml/*
i=0
for f in $FILES
do
    filename="_test_file.test"
    path="./test_files/"
    test_file=$path$i$filename
    python ./src/utils/test_creator/test_creator.py $f $test_file 40 ./src/utils/test_creator/replace_file.txt 
    ((i=i+1))
done