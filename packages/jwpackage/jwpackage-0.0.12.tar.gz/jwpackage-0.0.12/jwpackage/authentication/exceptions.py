class JwtExpiredError(Exception):
    def __init__(self,message="JWT token expired"):
        self.message = message
        super().__init__(self.message)

class TelegramIdMatchError(Exception):
    def __init__(self,message="Telegram id mismatch"):
        self.message = message
        super().__init__(self.message)

class AuthorizationFieldError(Exception):
    def __init__(self,message="No Authorization field in headers"):
        self.message = message
        super().__init__(self.message)