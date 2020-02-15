"""ETCD SETTINGS
Main class
"""

# # Native # #
from typing import Optional, Union

# # Installed # #
import etcd3.client
from etcd3 import Etcd3Client
from etcd3.watch import WatchResponse
from etcd3.events import PutEvent
from pydantic import BaseSettings

__all__ = ("ETCDSettings", "BaseETCDSettings",)


class ETCDSettings(BaseSettings):
    host: str
    port: int = 2739
    options: Optional[dict] = None
    etcd_client: Optional[Etcd3Client] = None
    watch: bool = False

    class Config:
        env_prefix = "ETCD_"

    def __init__(self, **kwargs):
        if kwargs.get("etcd_client"):
            kwargs["host"], kwargs["port"] = kwargs["etcd_client"]._url.split(":")

        super().__init__(**kwargs)

        if not self.etcd_client:
            self.etcd_client = etcd3.client(
                host=self.host,
                port=self.port,
                **self.options or {}
            )


ETCDDefinition = Union[ETCDSettings, Etcd3Client]


class BaseETCDSettings(BaseSettings):
    def __init__(self, etcd: ETCDDefinition, **kwargs):
        etcd_client: Etcd3Client

        if isinstance(etcd, ETCDSettings):
            etcd_client = etcd.etcd_client
        elif isinstance(etcd, Etcd3Client):
            etcd_client = etcd
        else:
            raise ValueError("ETCD not defined!")

        for field_name in self.__fields__.keys():
            field_value = etcd_client.get(field_name)[0]
            kwargs[field_name] = field_value

        super().__init__(**kwargs)
        self._etcd = etcd_client

        if etcd.watch:
            self._etcd_watch_id = self._etcd.add_watch_callback(
                key="\0",
                range_end="\0",
                callback=self._etcd_watch_callback
            )

    def __setattr__(self, name, value):
        self.Config.validate_assignment = True
        if name in ("_etcd", "_etcd_watch_id"):
            self.__dict__[name] = value
        else:
            super().__setattr__(name, value)

    def cancel_watch(self):
        watch_id = self.__dict__["_etcd_watch_id"]
        if watch_id:
            self._etcd.cancel_watch(watch_id)

    def _etcd_watch_callback(self, event_response: WatchResponse):
        for event in event_response.events:
            if isinstance(event, PutEvent):
                key = event.key.decode()
                value = event.value.decode()
                if key in self.__fields__.keys():
                    # TODO Not auto-parsing to attr type
                    # shall not use init again bc of hidden attrs
                    self.__setattr__(key, value)
