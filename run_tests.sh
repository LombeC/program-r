if [ -f "./results/errors.txt" ] 
then
    sudo rm ./results/errors.txt
fi

if [ -f "./results/empty.txt" ] 
then
    sudo rm ./results/empty.txt
fi

if [ -f "./results/successes.txt" ] 
then
    sudo rm ./results/successes.txt
fi
python ./src/utils/test_runner/test_runner.py --config ./bots/Ryan/config.yaml --cformat yaml --logging ./bots/Ryan/logging.yaml --test_dir ./test_files --qna_file ./src/utils/test_runner/qna-file