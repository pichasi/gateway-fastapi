# API Gateway Demo

## Instalation

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

1. Non-existant URL:
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