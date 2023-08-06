import json

from semantha_sdk.rest.rest_client import RestClient
from semantha_sdk.api.semantha_api import SemanthaAPI


__PLATFORM_SERVER_API_VERSION = "v3"


def login(server_url: str, key: str = None, key_file: str = None) -> SemanthaAPI:
    """ Access the Semantha API.

    Args:
        server_url (str): URL to the Semantha server
        key (str): A valid bearer token for accessing the given url.
        key_file (str): Path to a json file providing a valid `API_Key` value for the given url.

    Returns:
        SemanthaAPI: Entry point to the Semantha API.
    """
    __s = None
    if key:
        __s = SemanthaAPI(RestClient(server_url, key), f"/api/{__PLATFORM_SERVER_API_VERSION}")
    elif key_file:
        with open(key_file, "r") as key_file:
            __s = SemanthaAPI(RestClient(server_url, json.load(key_file)['API_Key']),
                              f"/api/{__PLATFORM_SERVER_API_VERSION}"
                              )
    else:
        raise ValueError("You need to supply an API key to login, either directly or via a file.")

    # check whether API key is valid or not
    __s.current_user.get()

    return __s
