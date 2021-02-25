# Cat or Dog - Simple ML Demo (with Azure Functions)

### Demo available here: http://catordogmldemo.azurewebsites.net
---

Simple demo of web application that can recognize animal (cat or dog) from a selected photography.
Created using Flask UWSGI Docker image (by [tiangolo](https://github.com/tiangolo)) and machine learning server ([code available here](https://github.com/crushyna/cat_or_dog_simple_ml_mlfunction)).

## Local installation
In order to run application locally, please:
1. Download both repositories (current and [machine learning server](https://github.com/crushyna/cat_or_dog_simple_ml_mlfunction)) to one directory
2. Make sure directories are ordered in this pattern:
+ parent_dir/cat_or_dog_simple_ml
+ parent_dir/cat_or_dog_simple_ml_mlfunction

3. Enter 'cat_or_dog_simple_ml' and run docker-compose (docker-compose build & docker-compose up)

Of course you can re-order and change directory structure. If so, be sure to revise docker-compose.yml.

## Local test
This application is equipped with collection of pytest / pylinter tests available to run locally.
In order to run them, please install the aplication locally in advance (p. Local installation), then:
1. Enter cat_or_dog_simple_ml directory
2. Make sure both repositories (webapp and ML server) are already built (docker-compose build)
3. Build test app: 
```
docker build -t cat_or_dog_simple_ml_tests:tester -f Dockerfile.tester --build-arg BaseImage=cat_or_dog_simple_ml_webapp . 
```
6. Now you can either test it using local or online ML Server (local is default). To run test locally, use:
```
docker run -it --rm -v ${PWD}:/data cat_or_dog_simple_ml_tests:tester
```
7. To test it online, use:
```
docker run -e ML_SERVER='<ml_server_addres>/api/MLServer' -it --rm -v  ${PWD}:/data cat_or_dog_simple_ml_tests:tester
```
When it's done, please feel free to revise results in folder cat_or_dog_simple_ml/test_reports

## Cloud deployment
Both repositories have their Dockerfile included. As far as web application (current repo) should be deployable at any cloud docker engine of your choice, ML Server has been created as dedicated Azure Function App, thus won't work anywhere else without proper code changes.

##### TODO: make ML Server available as docker container
