# wiremock-learning

Code for learning how to use wiremock

This will set up a toy flask app that evaluates an arithmetic expression using
a bunch of microservices.  This will allow for testing using wiremock to mock
different services.

## Requirements
This requires docker and docker-compose.yml.

## Usage

In order to run the calculator program:
* Build the image 
  ```
	docker build -t flask .
	```
* Use docker-compose to set up the program:
  ```
	docker-compose up
	```
* You can access the calculator program at 0.0.0.0:5000.

## Setup

The docker-compose.yml file will set up the containers for the project.
containers named "flask_[whatever]" are the program itself, while containers
named "[whatever]" are the wiremock proxies.

## Framework documentation

Flask and wiremock documentation can be found here:
* Flask - https://flask.palletsprojects.com/en/2.1.x/
* Wiremock - https://wiremock.org/docs/
