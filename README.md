# pydantic-etcd

![Test](https://github.com/David-Lor/pydantic-etcd/workflows/Test/badge.svg)

[pydantic](https://github.com/samuelcolvin/pydantic) BaseSettings - based class to load settings from an ETCD server.

**This image is experimental and might have undesirable effects. Currently is more a POC than a functional project.
Use it under your responsability!**

## Getting started

PUT these two keys in your ETCD server: `app_host` & `app_port` (int)

Then (assuming you're running an ETCD server on localhost), run:

```python
from pydantic_etcd import ETCDSettings, BaseETCDSettings

class MySettings(BaseETCDSettings):
    app_host: str
    app_port: int

etcd_settings = ETCDSettings(host="127.0.0.1", port=2739)
settings = MySettings(etcd_settings)

print("App host:", settings.app_host)
print("App port:", settings.app_port)
```

See more examples at [examples](examples).

## Changelog

- 0.0.1 - Initial version, load from ETCD and watch keys

## TODO

- Standarize priority of loading from environment variables and ETCD
- Support ETCD authentication (and other settings...)
- Support ETCD prefix

## Requirements

- Python >=3.6
- Requirements listed in [requirements.txt](requirements.txt)
- Running ETCD server

## Installing

While package is not uploaded to PyPi, can be installed with:

```bash
pip install git+git://github.com/David-Lor/pydantic-etcd.git#egg=pydantic-etcd
```

Or cloning the repo:

```bash
git clone https://github.com/David-Lor/pydantic-etcd.git
cd pydantic-etcd
python setup.py install
```

## Running tests

```bash
# Ensure you have a working ETCD server!

pip install -r requirements.txt
pip install -r requirements.test.txt

pytest .
```
