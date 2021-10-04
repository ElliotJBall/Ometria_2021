# Ometria_2021
Ometria Software engineer coding challenge 2021

### Testing
To run the test suite, run the following command:
```shell
python -m unittest
```

### Running the application

#### Using Docker
If you have docker installed, you can run the following commands:
```shell
docker build --tag elliot-ometria-coding-challenge-2021 .


# Either setup a .env environment file with the following:
MAILCHIMP_BASE_URL=
MAILCHIMP_API_KEY=
MAILCHIMP_LIST_ID=
OMETRIA_API_URL=
OMETRIA_API_KEY=
LOGGING_LEVEL=

docker run --rm -p 8080:8080 --env-file .env elliot-ometria-coding-challenge-2021

# Or pass them directly to the docker run command:

docker run --rm -p 8080:8080 -e MAILCHIMP_BASE_URL= -e MAILCHIMP_API_KEY= -e MAILCHIMP_LIST_ID= =e OMETRIA_API_URL= -e OMETRIA_API_KEY= LOGGING_LEVEL= elliot-ometria-coding-challenge-2021
```

#### Usage
For this coding challenge, I've set up a basic HTTP server that we will pretend is some consumer for a message broker, by sending a POST request we can trigger the running of an import/sync job for a given company/mailchimp listing id

To send the POST request you can use the following cURL snippet (The port dependany on your docker run command):
```shell
curl --location --request POST 'http://127.0.0.1:8080'
``` 