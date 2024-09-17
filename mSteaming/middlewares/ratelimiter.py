from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

class TimeWindowRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 200, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests #Limite par fenetre
        self.windowsize = window  #taille de la fenetre en secondes
        self.start_time = int(time.time()) # borne inf de la fenetre à t0
        self.currentwindowcounter = max_requests  #compteur de requetes par fenetre

    async def dispatch(self, request: Request, call_next):
        #get host ip
        request_time = int(time.time())
        print(f"Request time: {request_time}")
        print(f"Current window: [{self.start_time} : {self.start_time + self.windowsize}] ")
        print(f"Request remaining: {self.currentwindowcounter}")


        if request_time > self.start_time + self.windowsize:
            self.currentwindowcounter = self.max_requests
            self.start_time = int(time.time())

        if self.currentwindowcounter == 0:
            return JSONResponse(status_code=429, content={"error": "Too many requests"})

        self.currentwindowcounter -= 1
        return await call_next(request)
