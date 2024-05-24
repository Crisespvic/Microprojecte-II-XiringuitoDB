# Microprojecte II XiringuitoDB
Projecte per a l'assignatura de Base de Dades, es compòn d'una petita aplicació feta en Ubuntu20.04 i programada en Python 
i conectada a una base de dades de MongoDB creada en un contenidor de docker. 
L'aplicació pot realitzar registres de clients i diferents consultes.
També s'inclou una memòria descriptiva del projecte.

Per a poder instal.lar correctament i provar l'aplicació segueix els comandaments següents:

INSTRUCCIONS D'INSTAL.LACIÓ:

sudo apt install python3

sudo apt install python3-tk

sudo apt install python3-pip

sudo pip3 install pymongo

sudo snap install docker

sudo docker run -d \
    --name mongodb \
    -p 27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=admin \
    -e MONGO_INITDB_DATABASE=mydatabase \
    -v mongodb_data:/data/db \
    mongo:latest

INSTRUCCIONS D'EXECUCIÓ:

python3 xiringuito.py
