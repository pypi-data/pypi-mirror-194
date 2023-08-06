class RetarusSDKError(Exception):
    def __init__(self, message=None, http_message=None, http_status=None):

        if http_message is not None:
            self.http_message = http_message
            self.http_status = http_status
        if message is not None:
            self.message = message


class ApiAuthorizationError(RetarusSDKError):
    pass


class ApiInvalidPayload(RetarusSDKError):
    pass


class ConfigurationError(RetarusSDKError):
    pass


class SDKError(RetarusSDKError):
    pass

class RetarusRessourceNotFound(RetarusSDKError):
    pass