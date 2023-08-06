from __future__ import annotations
import typing
from urllib.parse import urljoin
from gloo_client.model import (
    CreateAppRequest,
    EmbeddingType,
    AppResponse,
    UpdateAppRequest,
    SearchResponse,
    SearchRequest,
)
from gloo_client.base_client import GlooBaseClient
from gloo_client.model.resources.app.app_list_response import AppListResponse
from gloo_client.model.resources.app.app_response_with_key import AppResponseWithKey
from gloo_client.model.resources.document.create_document_request import (
    CreateDocumentRequest,
)
from gloo_client.model.resources.document.document_annotation import DocumentAnnotation
from gloo_client.model.resources.document.document_content import DocumentContent
from gloo_client.model.resources.document.document_list_response import (
    DocumentListResponse,
)
from gloo_client.model.resources.document.document_query_id import DocumentQueryId

from gloo_client.model.resources.document.document_response import DocumentResponse
from gloo_client.model.resources.document.update_document_request import (
    UpdateDocumentRequest,
)


class ByDocumentId(typing.TypedDict):
    document_id: str


class BySource(typing.TypedDict):
    source: str


DocumentIdentifier = typing.Union[ByDocumentId, BySource]


class GlooAppClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient, app_id: str):
        super().__init__(
            origin=urljoin(base.origin, f"app/{app_id}"),
            app_secret=base.app_secret,
            headers=base.headers,
        )

    def app_get(self) -> AppResponse:
        return AppResponse.parse_raw(self._get("").text)

    def app_update(
        self,
        name: typing.Optional[str] = None,
        embeddings: typing.Optional[typing.List[EmbeddingType]] = None,
    ) -> AppResponse:
        return AppResponse.parse_raw(
            self._post("", data=UpdateAppRequest(name=name, embeddings=embeddings)).text
        )

    def search(
        self,
        query: str,
        *,
        max_content_size: typing.Optional[int] = None,
        tags: typing.Optional[typing.List[str]] = None,
        exclude_tags: typing.Optional[typing.List[str]] = None,
        alpha: typing.Optional[float] = None,
    ) -> SearchResponse:
        return SearchResponse.parse_raw(
            self._post(
                "search",
                data=SearchRequest(
                    query=query,
                    max_content_size=max_content_size,
                    included_tags=tags,
                    excluded_tags=exclude_tags,
                    alpha=alpha,
                    embedding=EmbeddingType.SBERT_MPNET_BASE_V_2,
                ),
            ).text
        )

    def document_create(
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
                "document/create",
                data=CreateDocumentRequest(
                    tags=tags or [],
                    name=name,
                    source=source,
                    content=c,
                    annotations=annotations,
                ),
            ).text
        )

    def document_get(self, _id: DocumentIdentifier) -> DocumentResponse:
        return DocumentResponse.parse_raw(
            self._get(
                "document",
                document_id=_id.get("document_id", None),
                source_id=_id.get("source", None),
            ).text
        )

    def document_delete(self, _id: DocumentIdentifier) -> None:
        if "document_id" in _id:
            _id = typing.cast(ByDocumentId, _id)
            idn = DocumentQueryId.factory.document_id(_id["document_id"])
        else:
            idn = DocumentQueryId.factory.source_id(_id["source"])
        self._delete("document", data=idn)

    def document_update(
        self,
        _id: DocumentIdentifier,
        *,
        name: typing.Optional[str] = None,
        source: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[str]] = None,
        annotations: typing.Optional[typing.List[DocumentAnnotation]] = None,
        content: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> DocumentResponse:
        c = (
            DocumentContent.factory.text(content)
            if isinstance(content, str)
            else DocumentContent.factory.chunks(content)
            if isinstance(content, list)
            else None
        )
        if "document_id" in _id:
            _id = typing.cast(ByDocumentId, _id)
            idn = DocumentQueryId.factory.document_id(_id["document_id"])
        else:
            idn = DocumentQueryId.factory.source_id(_id["source"])
        return DocumentResponse.parse_raw(
            self._post(
                "document",
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

    def document_get_all(self, *, page: int = 1) -> DocumentListResponse:
        return DocumentListResponse.parse_raw(
            self._get("document/list/all", page=page).text
        )
