#!/bin/bash
echo "Creating MongoDB database and importing data..."

# Initialize a new database and collection
mongo <<EOF
use $MONGO_INITDB_DATABASE
db.createCollection("yourCollectionName")
quit()
EOF

# Import the data into the new collection
mongoimport --db $MONGO_INITDB_DATABASE --collection yourCollectionName --type json --file /data/dataset_engineer.json --jsonArray --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD

