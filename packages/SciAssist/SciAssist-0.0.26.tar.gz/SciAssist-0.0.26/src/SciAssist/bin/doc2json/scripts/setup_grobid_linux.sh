#!/usr/bin/env bash

# put in your pdf2json directory here

export PDF2JSON_HOME="$( cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )"

echo $PDF2JSON_HOME
# Download Grobid
cd $HOME
wget https://github.com/kermitt2/grobid/archive/0.6.1.zip
unzip 0.6.1.zip
rm 0.6.1.zip
cd $HOME/grobid-0.6.1
./gradlew clean install

## Grobid configurations
# increase max.connections to slightly more than number of processes
# decrease logging level
# this isn't necessary but is nice to have if you are processing lots of files
cp $PDF2JSON_HOME/doc2json/grobid2json/grobid/config.yaml $HOME/grobid-0.6.1/grobid-service/config/config.yaml
cp $PDF2JSON_HOME/doc2json/grobid2json/grobid/grobid.properties $HOME/grobid-0.6.1/grobid-home/config/grobid.properties


