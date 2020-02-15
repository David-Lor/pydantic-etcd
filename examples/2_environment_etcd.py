"""ENVIRONMENT-VARIABLE DEFINED ETCD
Having the ETCD connection settings defined on environment variables.
Must run like this:
ETCD_HOST=127.0.0.1 ETCD_PORT=2739 python 2_environment_etcd.py
"""

from pydantic_etcd import ETCDSettings, BaseETCDSettings


class MySettings(BaseETCDSettings):
    app_host: str
    app_port: int


settings = MySettings(ETCDSettings())

print("App host:", settings.app_host)
print("App port:", settings.app_port)
