# Loop DB

The name means nothing. This is more of a template.

## Setup

Install redis on your machine. Docker is great.

Run Redis.

Install `pipenv` if you haven't already. Then run:

```
pipenv install
pipenv run python app.py
```

Voila!

----

## Endpoints

### Loop

The loop endpoint: `http://localhost:8080/loop`

Make a POST request to put data in redis.

URL: `http://localhost:8080/loop`  
Method: `POST`  
Body:
```
{
  "key": "test",
  "value": "this is a test"
}
```
Response:
```
{
  "status": "ok",
  "message": "'test' added to storage"
}
```

URL: `http://localhost:8080/loop?key=test`  
Method: `GET`  
Response:
```
{
  "status": "ok",
  "message": "this is a test"
}
```

### Dupe

The dupe endpoint: `http://localhost:8080/dupe`

Pretty much does nothing. It's here as an example how to make multiple 
resources/endpoints.

----

