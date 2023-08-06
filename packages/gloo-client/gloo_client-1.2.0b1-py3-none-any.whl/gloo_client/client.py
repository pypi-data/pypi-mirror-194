from __future__ import annotations
import typing

from gloo_client.environment import GlooEnvironment
from gloo_client.base_client import GlooBaseClient
from gloo_client.app_client import GlooAppClient
from gloo_client.model.resources.app.app_response import AppResponse
from gloo_client.model.resources.app.create_app_request import CreateAppRequest
from gloo_client.model.resources.common.embedding_type import EmbeddingType
from gloo_client.model.resources.app.app_list_response import AppListResponse


class GlooClient(GlooBaseClient):
    def __init__(
        self,
        app_secret: str,
        *,
        environment: typing.Union[str, GlooEnvironment] = GlooEnvironment.Production,
        headers: typing.Dict[str, str] = {},
    ):
        if isinstance(environment, str):
            origin = environment
        else:
            origin = environment.value
        super().__init__(origin=origin, app_secret=app_secret, headers=headers)

    def app_create(
        self, *, name: str, embeddings: typing.List[EmbeddingType]
    ) -> AppResponse:
        return AppResponse.parse_raw(
            self._post(
                "app", data=CreateAppRequest(name=name, embeddings=embeddings)
            ).text
        )

    def app_delete(self, *, app_id: str) -> None:
        self._delete(f"app/{app_id}", data=None)

    def app_get_all(self) -> AppListResponse:
        return AppListResponse.parse_raw(self._get("app/list/all").text)

    def app(self, *, app_id: str) -> GlooAppClient:
        return GlooAppClient(base=self, app_id=app_id)
