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


class AppClient(GlooBaseClient):
    def __init__(self, *, base: GlooBaseClient):
        super().__init__(
            origin=urljoin(base.origin, f"app"), app_secret=base.app_secret
        )

    def update(
        self,
        app_id: str,
        name: typing.Optional[str] = None,
        embeddings: typing.Optional[typing.List[EmbeddingType]] = None,
    ) -> AppResponse:
        return AppResponse.parse_raw(
            self._post(
                f"{app_id}", data=UpdateAppRequest(name=name, embeddings=embeddings)
            ).text
        )

    def get(self, app_id: str) -> AppResponse:
        return AppResponse.parse_raw(self._get(f"{app_id}").text)

    def search(
        self,
        app_id: str,
        query: str,
        *,
        max_content_size: typing.Optional[int] = None,
        tags: typing.Optional[typing.List[str]] = None,
    ) -> SearchResponse:
        return SearchResponse.parse_raw(
            self._post(
                f"{app_id}/search",
                data=SearchRequest(
                    query=query,
                    max_content_size=max_content_size,
                    included_tags=tags,
                    excluded_tags=None,
                    embedding=EmbeddingType.SBERT_MPNET_BASE_V_2,
                ),
            ).text
        )

    def create(
        self, name: str, embeddings: typing.List[EmbeddingType]
    ) -> AppResponseWithKey:
        return AppResponseWithKey.parse_raw(
            self._post("", data=CreateAppRequest(name=name, embeddings=embeddings)).text
        )

    def refresh_key(self, app_id: str) -> AppResponseWithKey:
        return AppResponseWithKey.parse_raw(
            self._post(f"{app_id}/refresh_key", data=None).text
        )

    def list_all(self) -> AppListResponse:
        return AppListResponse.parse_raw(self._get("list/all").text)

    def delete(self, app_id: str) -> None:
        self._delete(f"{app_id}", data=None)
