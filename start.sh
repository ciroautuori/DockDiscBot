#!/bin/bash

# Controlla se siamo nella directory corretta
if [ ! -d "docker" ]; then
    echo "Errore: Esegui lo script dalla directory principale del progetto"
    exit 1
fi

# Ferma eventuali container in esecuzione
docker-compose -f docker/docker-compose.yml down

# Ricostruisci e avvia
docker-compose -f docker/docker-compose.yml up --build 