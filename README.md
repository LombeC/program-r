## Introduction

Program R is an AIML interpreter written in Python. It includes an entire Python 3 framework for building you own chat bots using
Artificial Intelligence Markup Language, or AIML for short. This project was initially forked from [program-y](https://github.com/keiffster/program-y)

Program R is fully cross platform, running on:

- Linux
- Windows
- Mac OSX


## Installation
### Windows
To install program-r in windows you should do the following:

1- Clone the repository
```
git clone https://github.com/roholazandie/program-r.git
```

2- Install virtualenv for windows

3- after creating and activating virtualenv:
```
pip install -r requirements.txt
```

4- Open powershell or cmd and run:
```
set-executionpolicy RemoteSigned
```
Now you can run /env/Scripts/activate

5- Install spacy(if you are using nltk it's already installed in the previous part, no need to do this step):

-  Run powershell as admin in project directory

- Activate the environment:
```
python -m venv env
```
- Run:
```
./env/Scripts/activate
```
- Run:
```
pip install -U spacy
```
- Run:
```
/env/Scripts/python -m spacy download en
```
You should see the "linking successful" message.

4- [Install mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
 - If you want to change the default port number you have to consider changing it in your bot configuration in bot > database_config > port
 
5- download, extract and copy the [corenlp](https://stanfordnlp.github.io/CoreNLP/download.html) to the libs directory in root(after this you need to point to your specific version of corenlp in the config file of the bot you use in the section brain > nlp > corenlp > jar_dir)


6 - Set src:
- In pycharm:
    Right click on src then Mark as directory and then sources root

- In command line:
        Add src path to PYTHONPATH


### Linux

1 - Clone the repository:
```
git clone https://github.com/roholazandie/program-r.git
```

2- Install virtualenv for linux:
```
sudo apt-get install python3-pip
pip3 install virtualenv
```
3 - Create virtualenv named "env"(in the same directory as you cloned):
```
virtualenv -p python3 env
```

4- Activate virtualenv
```
source env/bin/activate
```

5- Install requirements
```
pip install -r requirements.txt
```

6- Install spacy (if you are using nltk it's already installed in the previous part, no need to do this step):
```
pip install -U spacy
python -m spacy download en
```

You should see the "linking successful" message.

7- [Install mongodb](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
 - If you want to change the default port number you have to consider changing it in your bot configuration in bot > database_config > port
 
8- download, extract and copy the [corenlp](https://stanfordnlp.github.io/CoreNLP/download.html) to the libs directory in root(after this you need to point to your specific version of corenlp in the config file of the bot you use in the section brain > nlp > corenlp > jar_dir)
 - Make sure you have Java 8.0 or higher installed for corenlp to work properly. Otherwise when checking sentinment an error will be thrown.
 - To check which version of java you have installed run:
    ```
    java -version
    ```
 - To install Java run:
    ```
    sudo apt-get update && apt-get upgrade
    sudo apt-get install default-jdk
    ```

9- Set src:
- In command line:
        Add src path to PYTHONPATH

- In pycharm:
    Right click on src then "Mark as directory" and then "Sources root"



## Points on using

1- the rephrase file should contain only one sentence phrases.

2- all templates should have the &lt;oob> tag except in the case where template has &lt;srai> tag. In this case, the template itself is just a pointer to another template and we don't need a separate robot tag.

3- if you use nltk as the nlp backend you have to create a nltk_data folder inside lib directory or any other place of your interest and point to that in config.yaml file. Otherwise after the first run of the program it will download the required data in your home directory.
## Running

Before running in windows you need to make sure that you have a "tmp" folder in the root of dive C:. This will keep track of
log files. In linux the folder is /tmp and is already there so you don't need any configuration.

There are different ways to run the programr based on your needs:

### Console run
Here we run tutorial bot in console mode:
```
python ./src/programr/clients/events/console/client.py --config ./bots/tutorial/config.yaml --cformat yaml --logging ./bots/tutorial/logging.yaml
```
### Majordomo run

```
python ./src/programr/clients/events/majordomo/client.py --config ./bots/tutorial/config.yaml --cformat yaml --logging ./bots/tutorial/logging.yaml
```

### Restful POST run

```
python ./src/programr/clients/restful/flask/client.py --config ./bots/tutorial/config.yaml --cformat yaml --logging ./bots/tutorial/logging.yaml
```
and to test it you can run (userid is unique and generated by the consumer to be able to run independent of other clients):
```
curl --header "Content-Type: application/json" --request POST --data '{"question":"hello","userid":123456}' http://localhost:5000/api/rest/v1.0/ask
```

## Docker

### Setting up Docker

First you need to create a network bridge between the docker container and the host. We are using 192.168.x.x subnet.
```
docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet
```

Then you need to create the docker image:
```
docker-compose build
```

It would be better if you create the image with a proper name:
```
docker build -t programr .
```
This will take some time. You can make sure that the image is created and has the name that you want by running `docker images`.

To run programr in this container:
```
docker run -it --rm --net=dockernet programr ./run.sh
```

### Making changes

If you want to change something in the image you can run:
```
docker run -it --net=dockernet programr /bin/bash
```
This will drop you into a terminal inside the container. You can now use `nano` to make your changes. After you are done you can run:
```
docker ps -l
```
and see the last change and its hash code, you can then commit the changes using:
```
docker commit -m "message for the commit" HASHCODE programr
```
note that you can also commit with a new name.

If you run `docker images` you should see all the images that you have.

### Running a precompiled image

If you just need to run programr and you are not going to change the code, you can just pull its latest image from dockerhub:
```
docker pull hojjat12000/program-r
```
If you run `docker images` you will see an image named `hojjat12000/program-r`. Make sure that you have create the network interface and named it `dockernet` (as instructed above).
Then run the image like so:
```
docker run -it --rm --net=dockernet hojjat12000/program-r ./run.sh
```
`--rm` will remove the new container created after you are done. Note that the image stays and you can just run the command above to run the program again.
