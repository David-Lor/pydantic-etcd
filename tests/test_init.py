"""TEST - INIT
"""

# # Native # #
import os

# # Installed # #
import pytest
import etcd3

# # Project # #
from pydantic_etcd import BaseETCDSettings, ETCDSettings

# # Package # #
from .helpers import BaseTest


class TestInit(BaseTest):
    """Test class initialization through all the available possibilities
    """
    
    def test_etcd_settings_object(self):
        """Test passing an instantiated ETCDSettings object
        """
        etcd_settings = ETCDSettings(
            host=self.settings.etcd_host,
            port=self.settings.etcd_port
        )
        settings = BaseETCDSettings(etcd_settings)

        assert settings._etcd._url == f"{etcd_settings.host}:{etcd_settings.port}"

    def test_etcd_settings_client(self):
        """Test passing an instantiated Etcd3Client object
        """
        etcd_client = etcd3.client(
            host=self.settings.etcd_host,
            port=self.settings.etcd_port
        )
        settings = BaseETCDSettings(etcd_client)

        assert settings._etcd._url == f"{self.settings.etcd_host}:{self.settings.etcd_port}"

    def test_etcd_settings_object_with_client(self):
        """Test passing an instantiated ETCDSettings object initialized with an Etcd3Client object
        """
        etcd_client = etcd3.client(
            host=self.settings.etcd_host,
            port=self.settings.etcd_port
        )
        etcd_settings = ETCDSettings(etcd_client=etcd_client)
        settings = BaseETCDSettings(etcd_settings)

        assert settings._etcd._url == f"{self.settings.etcd_host}:{self.settings.etcd_port}"
        assert etcd_settings.host == self.settings.etcd_host
        assert etcd_settings.port == self.settings.etcd_port

    def test_multiple_etcd_settings(self):
        """Test passing an instantiated ETCDSettings object to multiple BaseETCDSettings objects
        """
        etcd_settings = ETCDSettings(
            host=self.settings.etcd_host,
            port=self.settings.etcd_port
        )
        settings1 = BaseETCDSettings(etcd_settings)
        settings2 = BaseETCDSettings(etcd_settings)

        assert settings1._etcd is settings2._etcd
        assert settings1._etcd._url == f"{etcd_settings.host}:{etcd_settings.port}"

    def test_etcd_settings_object_from_env_variables(self):
        self.set_environment_variable("ETCD_HOST", self.settings.etcd_host)
        self.set_environment_variable("ETCD_PORT", self.settings.etcd_port)

        settings = BaseETCDSettings(ETCDSettings())

        assert settings._etcd._url == f"{self.settings.etcd_host}:{self.settings.etcd_port}"

    def test_etcd_settings_object_from_dotenv_file(self):
        dotenv_file_path = "/tmp/pydantic_etcd_test.env"

        with open(dotenv_file_path, "w") as dotenv_file:
            self.register_file(dotenv_file_path)
            dotenv_file.write(f"ETCD_HOST={self.settings.etcd_host}\n")
            dotenv_file.write(f"ETCD_PORT={self.settings.etcd_port}\n")
        
        class MyETCDSettings(ETCDSettings):
            class Config(ETCDSettings.Config):
                env_file = dotenv_file_path
        
        settings = BaseETCDSettings(MyETCDSettings())

        assert settings._etcd._url == f"{self.settings.etcd_host}:{self.settings.etcd_port}"

    def test_wrong_etcd_settings(self):
        """Test passing an invalid etcd init object to the BaseETCDSettings constructor
        """
        with pytest.raises(ValueError):
            BaseETCDSettings("127.0.0.1:2739")
