"""HARDCODED ETCD
Having the ETCD connection settings hardcoded
"""

from pydantic_etcd import ETCDSettings, BaseETCDSettings


class MySettings(BaseETCDSettings):
    app_host: str
    app_port: int


etcd_settings = ETCDSettings(host="127.0.0.1", port=2739)
settings = MySettings(etcd_settings)

print("App host:", settings.app_host)
print("App port:", settings.app_port)
