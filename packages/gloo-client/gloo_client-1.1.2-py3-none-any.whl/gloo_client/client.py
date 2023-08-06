from __future__ import annotations
import typing

from gloo_client.environment import GlooEnvironment
from gloo_client.base_client import GlooBaseClient
from gloo_client.app_client import AppClient
from gloo_client.document_client import DocumentClient


class GlooClient(GlooBaseClient):
    def __init__(
        self,
        environment: typing.Union[str, GlooEnvironment] = GlooEnvironment.Production,
        *,
        app_secret: str,
    ):
        if isinstance(environment, str):
            origin = environment
        else:
            origin = environment.value
        super().__init__(origin=origin, app_secret=app_secret)
        self.app = AppClient(base=self)

    def document(self, app_id: str) -> DocumentClient:
        return DocumentClient(base=self, app_id=app_id)
