from fastapi import FastAPI, Request, Depends
from .api_router import APIRouter, RouteNotFoundException, MethodNotAllowedException
app = FastAPI()

@app.api_route("{path_name:path}", methods=["GET", "POST", "DELETE", "PUT"])
async def route(request: Request, path_name: str, api_router: APIRouter = Depends(APIRouter)):

    try:
        response = await api_router.route(request=request)
        return response
    except RouteNotFoundException as rnfe:
        return {
            "unauthorized" : "No such route"
        }
    except MethodNotAllowedException as mnae:
        return {
            "unauthorized" : "Method not allowed"
        }