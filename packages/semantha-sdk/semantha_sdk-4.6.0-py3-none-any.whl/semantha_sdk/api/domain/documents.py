from __future__ import annotations

from io import IOBase

from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import DocumentSchema


class DocumentEndpoint(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/" + self._id

    def get(self):
        return self._session.get(self._endpoint).execute().to(DocumentSchema)


class DocumentsEndpoint(SemanthaAPIEndpoint):
    """ /api/{domainname}/documents endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documents"

    def post(
            self,
            file: IOBase = None,
            type: str = "similarity",
            document_type: str = None,
            with_areas: bool = False,
            with_context: bool = True,
            mode: str = "sentence",
            with_paragraph_type: bool = False
    ) -> list[DocumentEndpoint]:
        """ Create a document model

        Args:

            file (IOBase): Input document (as file)
            type (str): Enum: "similarity" "extraction". Choose the structure of a document
                for similarity or extraction. The type depends on the Use Case you're in.
            document_type (str): Specifies the document type that is to be used by semantha
                when reading the uploaded PDF document.
            with_areas (bool): Gives back the coordinates of referenced area.
            with_context (bool): Creates and saves the context.
            mode (str): Determine references: Mode to enable if a semantic search (fingerprint)
                or keyword search (keyword) should be considered. Creating document model: It also
                defines what structure should be considered for what operator (similarity or extraction).
            with_paragraph_type (bool): The type of the paragraph, for example heading, text.
        """
        return self._session.post(
            self._endpoint,
            body={
                "file": file,
                "type": type,
                "documenttype": document_type,
                "withareas": str(with_areas),
                "withcontext": str(with_context),
                "mode": mode,
                "with_paragraph_type": str(with_paragraph_type)
            }
        ).execute().to(DocumentSchema)

    def __call__(self, id: str):
        return DocumentEndpoint(self._session, self._endpoint, id)
