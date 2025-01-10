# API Gateway Demo

This is a simple implementation of an API Gateway using FastAPI. In another post, we will look at implementation using NodeJS, SpringBoot and others.

## Main components
1. backend: Maintained in backend folder
2. APIRouter: Maintained in api_router folder
3. APIRouter landing endpoint: Maintained in app/main.py

## How does it work

1. An API Request, such as /orders, lands on API Gateway port 8000.
2. main::route calls APIRouter::route method.
3. route method runs a series of validations to let the call pass through.

## Installation

Clone the repository
```bash
git clone https://github.com/pichasi/gateway-fastapi.git
```

## Usage

### Backend Application

From the root directory of the repo, run the backend application:

1. /orders endpoint in one shell:
```bash
uvicorn app.backend.main:app --host 0.0.0.0 --port 8002
```

2. /locations endpoint in another shell:
```bash
uvicorn app.backend.main:app --host 0.0.0.0 --port 8003
```

### API Gateway

From the root directory of the repo, run the API Gateway in another shell:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing the API Gateway with cURL

From another shell, run these commands one by one and see response:

1. Non-existent URL:
```bash
curl --location 'http://localhost:8000/doesnotexist'
```
Response
```json
{"unauthorized":"No such route"}
```
2. Direct backend call: Must not be allowed:
```bash
curl --location 'http://localhost:8003/locations'
```
Response
```json
{"unauthorized":"Unauthorized access"}
```
3. Locations call: Must be allowed and should be routed to locations service only.
```bash
curl --location 'http://localhost:8000/locations'
```
Response
```json
{"locations":["L1","L2"]}
```
4. Orders call: Must be allowed and should be routed to orders service only.
```bash
curl --location 'http://localhost:8000/orders'
```
Response
```json
{"orders":["O1","O2"]}
```