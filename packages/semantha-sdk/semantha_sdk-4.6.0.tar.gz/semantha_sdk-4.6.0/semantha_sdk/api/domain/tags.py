from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class DomainTagsEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/tags"

    def get(self) -> list[str]:
        """Get all tags that are defined for the domain"""
        return self._session.get(self._endpoint).execute().as_list()
