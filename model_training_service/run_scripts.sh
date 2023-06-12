#!/bin/bash

host_and_port="mongo:27017"

timeout=100

echo "Waiting for MongoDB to start..."
sleep 60
echo "MongoDB should be ready now, starting the Python scripts..."

python prep_data.py
python model_train.py
python recommend.py

