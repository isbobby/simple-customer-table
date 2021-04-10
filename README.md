# Getting Started with Docker
Ensure you have docker installed. The docker deployment uses a shell script entry file so you have to give it permission.

Go to services/customers and run `chmod +x entrypoint.sh`. This entrypoint file is executed to generate dummy data when docker-compose is executed.

Next, go back to the root directory where docker-compose.yml is located. You can review the docker-compose file to make changes to the ports if necessary. 

You can then build the container with 
`docker-compose -f docker-compose.yml up -d --build`

Another docker-compose file docker-compose.prod.yml is also provided. In which an nginx proxy is attached. You can run with `docker-compose -f docker-compose.prod.yml up -d --build`. 

Unlike development mode, running compose.dev will not generate dummy data.

## Files that you may want to review
__.env.dev/prod__

These provides app config details such as Database URI and Keys. In this repository they are exposed for convenience, you may wish to change these.

__Dockerfile__

They are the docker files for individual image. Automatic installing of python and its packages are done here. The python packages are stored in the requirements.txt

__entrypoint__ 

This is the script that runs when a docker-compose is successful. Right now, it checks if a database has been created, and creates one for you if there's no database created.
# Debugging without Docker
To debug/develop using localhost, go to services/customers and make slight changes to the following files

__project/config.py__

The Env files are exposed using docker-compose, you may wish to change to ENV variables to your own variables in this the config class. For example, you should change the database URI to that of your local database.

__myRedis.py__

The server runs redis on an image named 'redis', if you are starting your own redis service on localhost, you should change the localhost name to 'localhost' (make this change in project/init.py as well).

Once done, you can fire up localhost using `python3 app.py create_db` or `python3 app.py create_db_demo`(creates some dummy for you), and then `python3 app.py run`. You should also start a redis server on your localhost.

# API Routes and Implementation
You can list the routes using `python3 app.py routes`, this will expose the routes and their respective blueprint classes. 

You can see the collection of APIs and how to use them using the following link, it will bring you to the postman collection. 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.postman.co/run-collection/01a883b9bec6e5a8ad50?action=collection%2Fimport)
## Auth
/login `POST`
Retrieves customer username and password from the post request, then calls the ORM's check_hash to check if password matches. If so, return the access token to the customer.

/logout `DELETE`
Once a user chooses to logout, his JWT token will be stored in the Redis cache where all the expired tokens are stored. If a token is expired, users cannot use it to access restricted routes.
## Customer
/customers `GET` 
Gets all the customers in the database. Requires JWT token that is not expired.

/customers?numbers=n `GET` 
Gets N youngest customers in the database, sorting is done using sqlalchemy

/customers/delete?id=n `DELETE` 
First ensures that this customer exists in the database, then performs deletion using sqlalchemy and commit the session after sucsess.


/customers/create `POST`
Retrieves customer name and dob from request body and insert them in the database. The updated at field is updated using datetime.now()

/customers/update `POST`
Retrieves customer id, name and dob from request body and insert them in the database. It will search for hte customer for given ID first then then overwrites existing attributes.
## Defense against Replay Attack (stolen access token)
### Provision of session cookies
/session_cookie_experiment `GET`
A session ID is randomly generated and passed back to the user along with access token as aa cookie. This cookie is stored in the server side redis cache. When attackers try to access a route using the stolen token without the session cookie, we can detect there's a replay attack.

However, it only tackles very rare scenarios where the session id cookie is not also stolen. Hence it is not robust enough especially when the cookies might also get stolen by attackers.
### Rate limiting
A characteristic of replay attack is the high frequency of requests, a rate limiting declarator can be added to important routes to limit the rate of access. This can be done using python's rate limiter packages.

### Process ID
Instead of tagging the access token with a session ID, we can tag the process with a unique and random key to ensure there's always only one session.

# Testing
Testing is not done sufficiently on this project. Right now, a pytest package is installed and some simple tests are written in the tests directory. The next step will be 

Increase test coverage

Implement auto unit testing in docker-compose or other CI/CD pipelines


