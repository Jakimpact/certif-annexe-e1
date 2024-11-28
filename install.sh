#!/bin/bash

# Variables
VENV_DIR=".venv"
REQUIREMENTS_FILE="requirements.txt"


# Création et activation de l'environnement virtuel

# Vérification de la présence de Python
if ! command -v python3 &> /dev/null
then
    echo "Python3 n'est pas installé. Installez-le avant de continuer."
    exit 1
fi

# Création de l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    echo "Un environnement virtuel existe déjà dans le dossier $VENV_DIR."
else
    echo "Création de l'environnement virtuel dans $VENV_DIR..."
    python3 -m venv "$VENV_DIR"

    if [ $? -eq 0 ]; then
        echo "Environnement virtuel créé avec succès."
    else
        echo "Erreur lors de la création de l'environnement virtuel."
        exit 1
    fi
fi

# Activation de l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source "$VENV_DIR/bin/activate"

if [ $? -eq 0 ]; then
    echo "Environnement virtuel activé."
else
    echo "Erreur lors de l'activation de l'environnement virtuel."
    exit 1
fi


# Installation des requirements 

# Vérification de la présence de pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 n'est pas installé. Installez-le avant de continuer."
    exit 1
fi

# Installation des dépendances
echo "Installation des dépendances à partir de $REQUIREMENTS_FILE..."
pip3 install -r "$REQUIREMENTS_FILE"

# Vérification du succès de l'installation
if [ $? -eq 0 ]; then
    echo "Les dépendances ont été installées avec succès."
else
    echo "Erreur : Échec de l'installation des dépendances."
    exit 1
fi


# Installation de OBDC

# Vérification de la présence d'OBDC
if command -v odbcinst &>/dev/null; then
    echo "ODBC est déjà installé sur ce système."
    exit 0
else
    echo "ODBC n'est pas installé. Procédure d'installation en cours..."

    if ! [[ "18.04 20.04 22.04 23.04 24.04" == *"$(lsb_release -rs)"* ]];
    then
        echo "Ubuntu $(lsb_release -rs) is not currently supported.";
        exit;
    fi

    # Add the signature to trust the Microsoft repo
    # For Ubuntu versions < 24.04 
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
    # For Ubuntu versions >= 24.04
    curl https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg

    # Add repo to apt sources
    curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

    # Install the driver
    sudo apt-get update
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
    # optional: for bcp and sqlcmd
    sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
    source ~/.bashrc
    # optional: for unixODBC development headers
    sudo apt-get install -y unixodbc-dev

fi