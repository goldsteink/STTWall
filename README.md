# STTWall
Uses speech-to-text to take flac files and send text to the sink. It does so as a stateless, single worker topology, python-wallaroo application.

## Original Project
This project is simply adding a pre-existing project into wallaroo,
the original project can be found at: [speech-to-text-wavenet](https://github.com/buriburisuri/speech-to-text-wavenet "speech-to-text-wavenet")

### Citation
Kim and Park. Speech-to-Text-WaveNet. 2016. GitHub repository. https://github.com/buriburisuri/.

## Wallaroo
Please make sure you have followed these instructions: [python wallaroo](https://github.com/Sendence/wallaroo/blob/master/book/python/intro.md)

## Unzip
Please remember to unzip the files in the 'asset/train' directory
```
cd 'asset/train'
gunzip *.gz
```

## Running
```
nc -l 127.0.0.1 7002
machida --application-module sttwall --in 127.0.0.1:7010 --out 127.0.0.1:7002   --metrics 127.0.0.1:5001 --control 127.0.0.1:6000 --data 127.0.0.1:6001   --worker-name worker-name   --ponythreads=1
sender --host 127.0.0.1:7010 --file files.txt --batch-size 1 --interval 100_000_000 --messages 2000 --ponythreads=1
```


#### GCC 6
```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-6 g++-6 gcc-snapshot
sudo update-alternatives --install /usr/bin/gcc gcc \
  /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6
```
#### PIP
sudo apt-get install python-setuptools
sudo easy_install pip

#### Dependencies
```
sudo pip install --upgrade tensorflow
sudo pip install --upgrade sugartensor
sudo pip install --upgrade pandas
sudo pip install --upgrade librosa
````
