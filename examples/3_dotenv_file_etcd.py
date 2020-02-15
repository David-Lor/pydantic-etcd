"""DOTENV-FILE DEFINED ETCD
Having the ETCD connection settings defined on a dotenv file named .env
python-dotenv must be installed!

The .env file must look like this:

ETCD_HOST=127.0.0.1
ETCD_PORT=2379

"""

from pydantic_etcd import ETCDSettings, BaseETCDSettings


class MyETCDSettings(ETCDSettings):
    class Config(ETCDSettings.Config):
        env_file = ".env"


class MySettings(BaseETCDSettings):
    app_host: str
    app_port: int


settings = MySettings(ETCDSettings(host="127.0.0.1", port=2739))

print("App host:", settings.app_host)
print("App port:", settings.app_port)
