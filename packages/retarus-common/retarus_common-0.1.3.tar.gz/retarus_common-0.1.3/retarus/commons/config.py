from base64 import urlsafe_b64encode
from enum import Enum

from .region import Region


class Service(Enum):
    Sms = "sms"
    Fax = "fax"
    Webexpress = "webexpress"
    FaxInPoll = "faxinpoll"


class Configuration(object):
    region: Region = Region.Europe
    auth: dict = {}
    webexpress_auth_user_id: str = ""
    webexpress_auth_password: str = ""
    customer_number: str = ""

    @staticmethod
    def set_auth(user_id: str, password: str):
        """
        Set the credentials for a specify service.
        """
        auth_string = f"{user_id}:{password}"
        auth_string = urlsafe_b64encode(auth_string.encode('UTF-8')).decode('ascii')

        Configuration.auth = {"Authorization": f"Basic {auth_string}", "Content-Type": "application/json"}

    @staticmethod
    def set_webexpress_auth(user_id: str, password:str):
        """
        Set your webexpress credentails, so the sdk can interact with the webexpress service.
        """
        Configuration.webexpress_auth_user_id = user_id
        Configuration.webexpress_auth_password = password

    @staticmethod
    def set_region(region: Region):
        Configuration.region = region
