from fastapi import Request, Response
from fastapi.encoders import jsonable_encoder
from .exceptions import RouteNotFoundException, MethodNotAllowedException
from aiohttp import ClientSession

class APIRouter:

    def __init__(self):

        # TODO: Read this config from external configurable source
        
        self.config = {
            "endpoints": {
                "/orders": {
                    "methods": ["GET", "POST"],
                    # backend could be load balancer OR a list of backends registered automatically
                    # through a service discovery mechanism
                    "backend": "http://localhost:8002" # Load balancing by service
                },
                "/locations": {
                    "methods": ["GET", "POST"],
                    "backend": "http://localhost:8003" # Load balancing by service
                }
            },
        }

    async def route(self, request: Request):

        path = request.path_params["path_name"]
        # TODO: Log the critical parameters: Client IP, Timestamp etc. for monitoring and analytics

        # If a random path is accessed, don't forward to backend
        if path not in self.config["endpoints"]:
            # TODO: Log for audit
            raise RouteNotFoundException("Route not found")
        
        # If incorrect method for the path is accessed, don't forward to backend
        methods = self.config["endpoints"][path]["methods"]
        if request.method not in methods:
            # TODO: Log for audit
            raise MethodNotAllowedException(f"{request.method} not allowed")
        
        # TODO: Authentication/Authorization

        # TODO: Rate Limiter: Add a rate limiter here

        # TODO: Other restrictions

        # this is where the API is ready to be forwarded

        # Add API headers to the request so that backend can ensure the request is coming from APIGateway
        headers = request.headers.mutablecopy()

        # Send a JWT token from API Header here which backend can validate
        headers["gateway-jwt-token"] = "Some Security Header"

        # Route the request
        base_url = self.config["endpoints"][path]["backend"] + path
        
        async with ClientSession() as session:

            match request.method:
                # TODO: Pass all of the parameters and body
                case "GET":
                    response = await session.get(url=base_url, headers=headers)
                case "POST":
                    response = await session.post(url=base_url, data=request.body(), json=request.json(), headers=headers)
                # TODO: Other methods
                
            data = await response.content.read()
            modified_headers = response.headers.copy()
            self.add_headers(modified_headers)
            return Response(content=data, status_code=response.status, headers=modified_headers)
                
    def add_headers(self, modified_headers):
        # OWASP Secure Headers https://owasp.org/www-project-secure-headers/
        modified_headers['X-XSS-Protection'] = '1; mode=block'
        modified_headers['X-Frame-Options'] = 'DENY'
        modified_headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
        modified_headers['X-Content-Type-Options'] = 'nosniff'

        # Avoid Caching Tokens
        modified_headers['Expires'] = '0'
        modified_headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        modified_headers['Pragma'] = 'no-cache'