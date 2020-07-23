if [ -d "./test_files" ] 
then
    echo "Directory test_files exists." 
    sudo rm -r test_files
    mkdir test_files
else
    echo "Error: Directory test_files does not exists."
    mkdir test_files
fi

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

python ./src/utils/test_creator/test_creator.py --config ./bots/Ryan/config.yaml --aiml_file ./src/utils/test_runner/bot_test.aiml --test_file ./test_files/example.test --replace_file ./src/utils/test_creator/replace_file.txt --cformat yaml --logging ./bots/Ryan/logging.yaml