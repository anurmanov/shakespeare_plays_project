mongoimport /docker-entrypoint-initdb.d/shakespeare_plays.json --port 27017 --host 127.0.0.1 --db $DB_NAME --collection plays --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin