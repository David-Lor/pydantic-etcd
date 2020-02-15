"""TEST - WATCH
"""

# # Native # #
from time import sleep

# # Project # #
from pydantic_etcd import BaseETCDSettings, ETCDSettings

# # Package # #
from .helpers import BaseETCDTest


class TestWatch(BaseETCDTest):
    """Test creating a Settings class that must update its values from ETCD events
    """

    class MySettings(BaseETCDSettings):
        text: str
        number: int

    def test_watch_update_field(self):
        """Test having two values put on ETCD, initialize the settings class, and then put (update) them.
        The class attribute shall get updated with the latest value put on ETCD.
        """
        text = "text"
        number = 123

        self.etcd_put("text", text)
        self.etcd_put("number", number)
        
        etcd_settings = ETCDSettings(**self.etcd_settings.dict())
        etcd_settings.watch = True

        settings = self.MySettings(etcd_settings)
        
        assert settings.text == text
        assert settings.number == number

        new_text = "text updated"
        new_number = 987

        self.etcd_put("text", new_text)
        self.etcd_put("number", new_number)
        sleep(1)

        assert settings.text == new_text
        assert settings.number == new_number

    def test_watch_update_field_wrong_value(self):
        """Test having two values put on ETCD, initialize the settings class, and then put (update) them, one having an invalid value.
        The class attribute shall remain unchanged.
        """
        text = "text"
        number = 123

        self.etcd_put("text", text)
        self.etcd_put("number", number)

        etcd_settings = ETCDSettings(**self.etcd_settings.dict())
        etcd_settings.watch = True

        settings = self.MySettings(etcd_settings)

        assert settings.text == text
        assert settings.number == number

        new_text = "text updated"
        new_number = "not a number"

        self.etcd_put("text", new_text)
        self.etcd_put("number", new_number)
        sleep(1)

        assert settings.text == new_text
        assert settings.number == number
