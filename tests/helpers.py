"""HELPERS
Helpers and base test classes for the tests
"""

# # Native # #
import os
from typing import Set

# # Installed # #
import etcd3
from pydantic import BaseSettings

# # Project # #
from pydantic_etcd import BaseETCDSettings, ETCDSettings

__all__ = ("BaseTest", "BaseETCDTest")


class TestSettings(BaseSettings):
    etcd_host: str = "127.0.0.1"
    etcd_port: int = 2739

    class Config:
        env_prefix = "TEST_"
        env_file = "test.env"


class BaseTest:
    settings: TestSettings
    created_files: Set[str]
    set_env_vars: Set[str]

    def setup_method(self):
        self.settings = TestSettings()
        self.created_files = set()
        self.set_env_vars = set()
    
    def teardown_method(self):
        for created_file in self.created_files:
            os.remove(created_file)
        for set_env_var in self.set_env_vars:
            os.environ.pop(set_env_var)

    def set_environment_variable(self, key, value):
        os.environ[key] = str(value)
        self.set_env_vars.add(key)
    
    def register_file(self, file_path):
        self.created_files.add(file_path)


class BaseETCDTest(BaseTest):
    etcd_settings: ETCDSettings
    put_keys: Set[str]

    def setup_method(self):
        super().setup_method()
        self.etcd_settings = ETCDSettings(
            host=self.settings.etcd_host,
            port=self.settings.etcd_port
        )
        self.put_keys = set()

    def teardown_method(self):
        super().teardown_method()
        for key in self.put_keys:
            self.etcd_settings.etcd_client.delete(key)

    def etcd_put(self, key, value):
        self.etcd_settings.etcd_client.put(key, str(value))
        self.put_keys.add(key)
