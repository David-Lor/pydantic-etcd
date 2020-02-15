"""TEST - READ
"""

# # Installed # #
import pytest
from pydantic import ValidationError

# # Project # #
from pydantic_etcd import BaseETCDSettings

# # Package # #
from .helpers import BaseETCDTest


class TestRead(BaseETCDTest):
    """Test creating a Settings class that must read its attributes from ETCD
    """

    class MySettings(BaseETCDSettings):
        text: str
        number: int

    def test_read_etcd_settings(self):
        """Test reading settings existing on ETCD
        """
        text = "text"
        number = 123

        self.etcd_put("text", text)
        self.etcd_put("number", number)

        settings = self.MySettings(self.etcd_settings)
        
        assert settings.text == text
        assert settings.number == number

    def test_read_etcd_settings_missing(self):
        """Test reading settings when one of them is missing from ETCD
        """
        self.etcd_put("text", "text")

        with pytest.raises(ValidationError):
            self.MySettings(self.etcd_settings)
