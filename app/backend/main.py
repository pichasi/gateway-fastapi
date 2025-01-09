from fastapi import FastAPI, Request

app = FastAPI()

LOCATIONS = ["L1", "L2"]
ORDERS = ["O1", "O2"]

@app.get("/locations")
async def locations(request: Request):

    if "gateway-jwt-token" not in request.headers:
        return {
            "unauthorized" : "Unauthorized access"
        }
    
    return {
        "locations" : LOCATIONS
    }
    
@app.get("/orders")
async def orders(request: Request):

    if "gateway-jwt-token" not in request.headers:
        return {
            "unauthorized" : "Unauthorized access"
        }
    
    return {
        "orders" : ORDERS
    }