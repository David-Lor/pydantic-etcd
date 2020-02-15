"""ENVIRONMENT-VARIABLE DEFINED ETCD - MULTIPLE CLASSES
Having the ETCD connection settings defined on environment variables.
Must run like this:
ETCD_HOST=127.0.0.1 ETCD_PORT=2739 python 2_environment_etcd.py

This example shows how we can use the same ETCD connection for multiple settings classes
"""

from pydantic_etcd import ETCDSettings, BaseETCDSettings


class AppSettings(BaseETCDSettings):
    host: str
    port: int

    class Config:
        env_prefix = "APP_"


class MongoSettings(BaseETCDSettings):
    host: str
    port: int
    database: str
    collection: str

    class Config:
        env_prefix = "MONGO_"


etcd_settings = ETCDSettings()
app_settings = AppSettings(etcd_settings)
mongo_settings = MongoSettings(etcd_settings)

print("App host:", app_settings.app_host)
print("App port:", app_settings.app_port)
print("Mongo host:", mongo_settings.host)
print("Mongo port:", mongo_settings.port)
print("Mongo database:", mongo_settings.database)
print("Mongo collection:", mongo_settings.collection)
