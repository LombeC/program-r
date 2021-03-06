if [ -d "./test_files" ] 
then
    echo "Directory test_files exists." 
    sudo rm -r test_files
    mkdir test_files
else
    echo "Error: Directory test_files does not exists."
    mkdir test_files
fi

FILES=./bots/Ryan/aiml/*
i=0

if [ -f "./results/failed_loads.txt" ] 
then
    sudo rm ./results/failed_loads.txt
fi

if [ -f "./results/questions.txt" ] 
then
    sudo rm ./results/questions.txt
fi

if [ -f "./results/responses.txt" ] 
then
    sudo rm ./results/responses.txt
fi

for f in $FILES
do
    basename=$(basename $f)
    echo "basename: " $basename
    extension=".tests"
    path="./test_files/"
    test_file=$path$basename$extension
    python ./src/utils/test_creator/test_creator.py --config ./bots/Ryan/config.yaml --aiml_file $f --test_file $test_file --replace_file ./src/utils/test_creator/replace_file.txt --cformat yaml --logging ./bots/Ryan/logging.yaml
    ((i=i+1))
done