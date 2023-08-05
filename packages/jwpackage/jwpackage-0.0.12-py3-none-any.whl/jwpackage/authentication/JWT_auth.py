import time
from jwpackage.authentication.auth  import Authenticator
from fastapi import HTTPException,Request,status
from fastapi.responses import JSONResponse
from jwpackage.authentication.exceptions import AuthorizationFieldError



# class JWTAuthenticate:
#     def __init__(self,public_key,request):
#         self.public_key = public_key
#         self.request = request
#         credentials = self.request.headers.get("Authorization")
#         bearer,token = credentials.split()
#         if bearer.lower() != "bearer":
#             raise HTTPException(status_code=401, detail="token must be prefixed with 'bearer'")
#         auth = Authenticator(self.public_key,token,self.request)
#         if not auth.is_authenticated():
#             raise HTTPException(status_code=401, detail="Unauthorized")

# def authenticate(pub_key,request):
#     """
#     decodes token in request headers and verifies it
#     raise Exception if token exprired or tID does not match
#     """
#     credentials = request.headers.get("Authorization")
#     bearer,token = credentials.split()
#     if bearer.lower() != "bearer":
#         raise HTTPException(status_code=401, detail="token must be prefixed with 'bearer'")
#     auth = Authenticator(pub_key,token,request)
#     if not auth.is_authenticated():
#         raise HTTPException(status_code=401, detail="Unauthorized")

# async def authenticate_middleware(pub_key,request: Request, call_next):
#     start_time = time.time()

#     credentials = request.headers.get("Authorization")
#     bearer,token = credentials.split()  
#     if bearer != "Bearer":
#         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
#     auth = Authenticator(pub_key,token,request)
#     if not auth.is_authenticated():
#         return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

class JWTAuthenticate:
    def __init__(self,pub_key,skip_paths:list):
        self.public_key = pub_key
        self.skip_paths = skip_paths
    async def authenticate_middleware(self,request: Request,request_body, call_next):
        try:
            start_time = time.time()
            current_path =  request.scope["path"]

            print("current path: %s" % current_path)
            for path in self.skip_paths:
                if current_path.endswith(path):
                    return await call_next(request)
            if "Authorization" not in request.headers:
                raise AuthorizationFieldError()
            credentials = request.headers.get("Authorization")
            bearer,token = credentials.split()  
            if bearer != "Bearer":
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
            auth = Authenticator(self.public_key,token,request_body)
            if not auth.is_authenticated():
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except AuthorizationFieldError as e:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "No authorization field in header"})
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
    
    def authenticate_path(self,request):
        """
        decodes token in request headers and verifies it
        raise Exception if token exprired or tID does not match
        """
        credentials = request.headers.get("Authorization")
        bearer,token = credentials.split()
        if bearer.lower() != "bearer":
            raise HTTPException(status_code=401, detail="token must be prefixed with 'bearer'")
        auth = Authenticator(self.public_key,token,request)
        if not auth.is_authenticated():
            raise HTTPException(status_code=401, detail="Unauthorized")