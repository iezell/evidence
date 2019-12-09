# Object Report

A proof of concept for model tracking and reporting.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
For Django Project:
  Docker
  Docker-Compose
  Virtualenv
```

### Installing

A step by step series of examples that tell you how to get a development env running

```
#From Root Directory EvidenceCare
docker-compose build
docker-compose up
```
This should spawn three containers:
1. Mongodb: exposed through the localhost:27017
2. Mongo-Express: exposed on http://0.0.0.0:8081/ (view objectreport at http://0.0.0.0:8081/db/objectreport)

## Running the tests

To run a test script:

```
#From Root Directory EvidenceCare
python3 -m venv EvidenceCare
mkdir EvidenceCare/project
cp -r EvidenceCare/project
source EvidenceCare/bin/activate
pip3 install -r projects/requirements
cd projects
python manage.py test

#To view, go to http://0.0.0.0:8081/db/objectreport/report and the test models should be visable
```

## Notes

Thanks for taking the time to evaluate my code! I choose Django and Mongo based off my knowledge of EvidenceCare's techstack.
Hopefully everything was able to spin up correctly and pretty easy if docker, docker-compose, and Virtualenv are installed. I took a few
liberties when deciding how to set this up:

  1. Mongo - Give the volatility of objects within Python, I think reddis maybe a better choice as a    database given how fast
             it is compared to mongo. This could even be setup to purge old entries after a certain time or volume that would
             be beneficial. There is a sqlite database in use. This could be moved entirely to mongo but there would probably be a
             lose of performance having to do a transaction between mongodb to add a new entry instead of having a cache of the
             local objects

  2. Threading - As this was a proof of concept, I focused on functionality over bells and whistles. I think to successfully
                 implement this feature, a more robust Identifier would have to be figured out. One solution would be to implement
                 tokenization, that way third party models could also be tracked more easily.


  3. Containerization - I had planned on containerizing the django project, but I burned the midnight oil to get this done so thats
                        more of a ToDo.

  4. API - Obviously this would be a nice to have. Given that this project essentially just post to a mongodb, the front end could be
           made into a Restful API to handle Get, Post, Put, and Delete functionality. While we could set it up to handle inherit models,
           this could also be set up as a service and simply just make a request to provide whatever action the end user wants. 


## Built With

* [Django] - The web framework
* [Mongo] - Database

## Authors

* **Ian Ezell**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
