docker-compose up -d --build

to create the database, run
docker-compose exec customer python app.py create_db

view the created databse via
docker-compose exec db psql --username=klinify --dbname=customer_table

Ceck that the volumn was created by running
docker volume inspect simple-customer-table_postgres_data

Entry point.sh is created to ensure postgres is up and healthy before
creating the database table

run chmod +x entrypoint.sh to update the file permission too

Dockerfile.prod is created for production builds

$ docker-compose -f docker-compose.prod.yml down -v
$ docker-compose -f docker-compose.prod.yml up -d --build
$ docker-compose -f docker-compose.prod.yml exec customer python3 app.py create_db

## file descriptions
### .env.dev/.env.prod
Contains environment variable for both development/production, but right now they are identical

### docker-compose.prod.yml
Docker compose build file for production build, build using the following commands
\br docker-compose -f docker-compose.prod.yml up -d --build

### docker-compose.yml
Docker compose build file for development build
\br docker-compose -f docker-compose.yml up -d --build

### entrypoint.prod.sh
Scripts to be executed when a production build is finished
\br Give this file permission using chmod -x entrypoint.prod.sh
