"""HARDCODED ETCD CLIENT
Having the ETCD client object initialized (hardcoded)
"""

import etcd3
from pydantic_etcd import BaseETCDSettings


class MySettings(BaseETCDSettings):
    app_host: str
    app_port: int


etcd_client = etcd3.client(host="127.0.0.1", port=2379)
settings = MySettings(etcd_client)

print("App host:", settings.app_host)
print("App port:", settings.app_port)
