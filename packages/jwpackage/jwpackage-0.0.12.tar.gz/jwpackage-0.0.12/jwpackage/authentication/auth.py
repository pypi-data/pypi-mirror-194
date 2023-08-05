import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwpackage.authentication.exceptions import *
import time
from datetime import datetime
class Authenticator():
    def __init__(self,public_key,token,request):
        self.request = request
        self.public_key = serialization.load_pem_public_key(
            public_key,
            backend=default_backend()
        )
        print("public key",self.public_key)
        try:
            self.data = jwt.decode(token, public_key,algorithms=["RS256"],audience="justwicks")
            self.auth = True
            # print(self.data)
            # self.validate_telegram_id()
        except jwt.exceptions.DecodeError as err:
           self.custom_exception_handler(err)

    def custom_exception_handler(self,e):
        print("Authentication Failed: %s" % e)
        self.auth = False
    
    def validate_telegram_id(self):
        try:
            if str(self.data["tId"]) == str(self.request.get("tId")):
                self.auth = True
            else:
                raise TelegramIdMatchError()
        except Exception as e:
            self.custom_exception_handler(e)
    
    def is_authenticated(self):
        return self.auth






