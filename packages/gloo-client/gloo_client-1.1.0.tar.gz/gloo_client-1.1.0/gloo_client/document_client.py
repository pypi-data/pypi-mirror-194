from __future__ import annotations
import typing
from urllib.parse import urljoin
from gloo_client.model import (
    DocumentResponse,
    UpdateDocumentRequest,
    CreateDocumentRequest,
    DocumentContent,
    DocumentAnnotation,
    DocumentListResponse,
)
from gloo_client.base_client import GlooBaseClient
from gloo_client.model.resources.document.document_query_id import DocumentQueryId


class ByDocumentId(typing.TypedDict):
    document_id: str


class BySource(typing.TypedDict):
    source: str


DocumentIdentifier = typing.Union[ByDocumentId, BySource]


class DocumentClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, app_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"app/{app_id}/document"),
            app_secret=base.app_secret,
        )

    def create(
        self,
        *,
        name: str,
        source: str,
        content: typing.Union[str, typing.List[str]],
        annotations: typing.Optional[typing.List[DocumentAnnotation]] = None,
        tags: typing.Optional[typing.List[str]] = None,
    ) -> DocumentResponse:
        c = (
            DocumentContent.factory.text(content)
            if isinstance(content, str)
            else DocumentContent.factory.chunks(content)
            if isinstance(content, list)
            else None
        )

        return DocumentResponse.parse_raw(
            self._post(
                "",
                data=CreateDocumentRequest(
                    tags=tags or [],
                    name=name,
                    source=source,
                    content=c,
                    annotations=annotations,
                ),
            ).text
        )

    def update(
        self,
        idf: DocumentIdentifier,
        *,
        name: typing.Optional[str],
        source: typing.Optional[str],
        tags: typing.Optional[typing.List[str]],
        annotations: typing.Optional[typing.List[DocumentAnnotation]],
        content: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> DocumentResponse:
        c = (
            DocumentContent.factory.text(content)
            if isinstance(content, str)
            else DocumentContent.factory.chunks(content)
            if isinstance(content, list)
            else None
        )
        if "document_id" in idf:
            idn = DocumentQueryId.factory.document_id(idf["document_id"])
        else:
            idn = DocumentQueryId.factory.source_id(idf["source"])
        return DocumentResponse.parse_raw(
            self._post(
                "",
                data=UpdateDocumentRequest(
                    query=idn,
                    name=name,
                    content=c,
                    tags=tags,
                    annotations=annotations,
                    source=source,
                ),
            ).text
        )

    def list_all(self, page: int = 1) -> DocumentListResponse:
        return DocumentListResponse.parse_raw(self._get("list/all", page=page).text)

    def delete(self, idf: DocumentIdentifier) -> None:
        if "document_id" in idf:
            idn = DocumentQueryId.factory.document_id(idf["document_id"])
        else:
            idn = DocumentQueryId.factory.source_id(idf["source"])
        self._delete("", data=idn)

    def get(self, idf: DocumentIdentifier) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._get(
                "",
                document_id=idf.get("document_id", None),
                source_id=idf.get("source", None),
            ).text
        )
