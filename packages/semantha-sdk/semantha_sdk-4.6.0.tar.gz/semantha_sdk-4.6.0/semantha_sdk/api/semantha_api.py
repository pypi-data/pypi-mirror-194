from __future__ import annotations

from semantha_sdk.api.current_user import CurrentUserEndpoint
from semantha_sdk.api.diff import DiffEndpoint
from semantha_sdk.api.domain import DomainsEndpoint
from semantha_sdk.api.model import ModelEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient


class SemanthaAPI(SemanthaAPIEndpoint):
    """ Entry point to the Semantha API.

        References the /currentuser, /domains and /diff endpoints.

        Note:
            The __init__ method is not meant to be invoked directly
            use `semantha_sdk.login()` with your credentials instead.
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__current_user = CurrentUserEndpoint(session, self._endpoint)
        self.__diff = DiffEndpoint(session, self._endpoint)
        self.__domains = DomainsEndpoint(session, self._endpoint)
        self.__model = ModelEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint

    @property
    def current_user(self) -> CurrentUserEndpoint:
        return self.__current_user

    @property
    def domains(self) -> DomainsEndpoint:
        return self.__domains

    @property
    def diff(self) -> DiffEndpoint:
        return self.__diff

    @property
    def model(self) -> ModelEndpoint:
        return self.__model
