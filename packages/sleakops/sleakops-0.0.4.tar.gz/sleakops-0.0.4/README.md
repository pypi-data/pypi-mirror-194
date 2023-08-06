# How to install

Generate environment file

`
cp local.env .env
`

## Run a build

`
docker compose run cli python sleakops.py build --project core --branch qa --wait
`

## Run a deployment

`
docker compose run cli python sleakops.py deployment --project core --branch qa --wait
`

### Run help

`
docker compose run cli python sleakops.py --help 
`