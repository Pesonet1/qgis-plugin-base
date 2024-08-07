from typing import Any

from qgis.PyQt.QtNetwork import QNetworkReply

from plugin.utilities.i18n import translate


class BasePluginException(Exception):
    """Base class for all Example plugin exceptions.

    All other exception are derived from this custom exception class.

    Args:
        Exception (_type_): Python base exception class

    Returns:
        _type_: _description_
    """

    default_message = translate("exceptions", "baseException")

    def __init__(
        self,
        message: str | None = None,
        bar_msg: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Add message bar to the QGIS UI about the exception and log the error
        before proceeding as with any other exception.

        Args:
            message (str): Exception message.
            duration (int | None, optional): Duration of time that the
                message bar will be show in seconds. Use None to keep until
                cleared by user. Defaults to None.
        """
        if message is None:
            message = self.default_message

        self._message: str = message

        super().__init__(message)

        self.bar_msg: dict[str, Any] = bar_msg if bar_msg is not None else {}


class GenericException(BasePluginException):
    default_msg = translate("exceptions", "genericError")


class UnkownException(BasePluginException):
    default_msg = translate("exceptions", "unkownError")


class NetworkException(BasePluginException):
    default_msg = translate("exceptions", "networkError")

    def __init__(
        self,
        *args: Any,
        error: QNetworkReply.NetworkError | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the exception with error details so the plugin may process
        different network exceptions differently.
        :param status: The QNetworkReply error type
        """
        self.error = error
        super().__init__(*args, **kwargs)


class ConfigurationException(BasePluginException):
    """Invalid plugin configuration exception."""

    @property
    def exception_class(self) -> str:
        """Get exception type as translated string."""
        return translate("exceptions", "configException")
