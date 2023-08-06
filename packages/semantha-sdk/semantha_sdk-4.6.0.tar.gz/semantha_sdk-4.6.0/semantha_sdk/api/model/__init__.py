from semantha_sdk.api.domain.model import DomainModelsEndpoint, DomainModelEndpoint
from semantha_sdk.api.model.extractor_types import ExtractorTypesEndpoint
from semantha_sdk.api.metadata_types import MetadataTypesEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient


class ModelEndpoint(SemanthaAPIEndpoint):
    """
        api/model endpoint

        References: datatypes, domains, exctractortypes, metadatatypes
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__model_domains = DomainModelsEndpoint(session, self._endpoint)
        self.__extractor_types = ExtractorTypesEndpoint(session, self._endpoint)
        self.__metadata_types = MetadataTypesEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/model"

    @property
    def domains(self):
        return self.__model_domains

    @property
    def extractor_types(self):
        return self.__extractor_types

    @property
    def metadata_types(self):
        return self.__metadata_types

    def __call__(self, domain: str) -> DomainModelEndpoint:
        return DomainModelEndpoint(self._session, self._endpoint, domain)
