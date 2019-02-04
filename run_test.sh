#!/usr/bin/env bash

if [ -z ${1} ]; then
    echo "Your api key needs to be added as an argument"
    exit 1
fi

echo "Exporting the api_key as an environment variable"
export TMDB_KEY=${1}

# Create (if needed) and activate the virtual environment
if [ ! -d "env" ]; then
    echo "Creating the virtual environment"
    virtualenv -q env
else
    EXISTS="true"
fi

echo "Activating the virtual environment"
source env/bin/activate

# Use pip to install the requirements
{
    if [ "$EXISTS" != "true" ]; then
        echo "Installing required packages"
        pip2 install -r requirements.txt
    fi
} || { # This code with run if the previous fails
    pip install -r requirements.txt
}

echo "Running the tests"
nosetests tests/api_tests.py

echo "Deactivating the environment"
deactivate

echo "Removing the api_key environment variable"
unset TMDB_KEY