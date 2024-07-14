# Backend Challenge 

<br>


## Setup

#### Pre-requisites
- Docker Desktop
- Git

#### Installation
- Go to the project directory in the terminal.
```bash
make start 
```

- Initialize database
```bash
make init_db
```

- Load csv file (files copied to the data folder)
```bash 
make load_csv FILENAME=sample.csv
```

## Run server
This will serve the apis on the port 9010.
```bash
make serve 
```

## Swagger UI 
Swagger UI - [http://localhost:9010/docs](http://localhost:9010/docs)


## Unit testing 
```bash
make test 
```

<br>

## Cleanup
- Remove tables from the database (in case, you want to create factories again.)
```bash
make clean_db
```

- Clean docker setup.
```bash
make clean
```