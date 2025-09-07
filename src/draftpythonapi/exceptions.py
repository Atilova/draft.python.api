class BaseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

        self.message = message


class InfrastructureError(BaseError): ...
class ApplicationError(BaseError): ...
class BusinessError(BaseError): ...
