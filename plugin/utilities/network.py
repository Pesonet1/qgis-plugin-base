import json
from typing import Literal, NamedTuple

from qgis.core import (
    Qgis,
    QgsBlockingNetworkRequest,
    QgsNetworkReplyContent,
)
from qgis.PyQt.QtCore import QSettings, QUrl
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

from plugin.exceptions import NetworkException
from plugin.utilities.message_builder import MessageBuilder
from plugin.utilities.resources import get_plugin_name


class FileInfo(NamedTuple):
    file_name: str
    content: bytes
    content_type: str


class FileField(NamedTuple):
    field_name: str
    file_info: FileInfo


def get(
    url: str,
) -> bytes:
    """Get request

    Args:
        url (str): resource address

    Returns:
        bytes: request content in bytes
    """
    return request_raw(url, "get")


def post(
    url: str,
    data: dict[str, str] | None = None,
) -> bytes:
    """Post request

    Args:
        url (str): resource address
        data (dict[str, str] | None): request body.
            Defaults to None.

    Returns:
        bytes: request content in bytes
    """
    return request_raw(url, "post", data)


def set_request_headers(req: QNetworkRequest):
    # http://osgeo-org.1560.x6.nabble.com/QGIS-Developer-Do-we-have-a-User-Agent-string-for-QGIS-td5360740.html
    user_agent = QSettings().value(
        "/qgis/networkAndProxy/userAgent", "Mozilla/5.0"
    )
    user_agent += " " if len(user_agent) else ""
    user_agent += f"QGIS/{Qgis.QGIS_VERSION_INT}"
    user_agent += f" {get_plugin_name}"

    req.setRawHeader(b"User-Agent", bytes(user_agent, "utf-8"))

    return req


def request_raw(
    url: str,
    method: Literal["get", "post"] = "get",
    data: dict[str, str] | None = None,
) -> bytes:
    """Network request wrapper using QgsBlockingNetworkRequest. It is
    recommended way to make external requests from QGIS

    Args:
        url (str): resource address
        method (Literal["get", "post"]): request method.
            Defaults to "get".
        data (dict[str, str] | None, optional): post request body.
            Defaults to None.

    Raises:
        Exception: _description_
        QgsNetworkException: _description_

    Returns:
        bytes: request content in bytes
    """
    req = QNetworkRequest(QUrl(url))
    set_request_headers(req)

    # QgsApplication.instance().authManager().updateNetworkRequest(
    #     req, AUTH_CONFIG_ID
    # )

    request_blocking = QgsBlockingNetworkRequest()

    if method == "get":
        _ = request_blocking.get(req)
    elif method == "post":
        if data:
            # Support JSON
            byte_data = bytes(json.dumps(data), "utf-8")
            req.setRawHeader(
                b"Content-Type",
                bytes("application/json; charset=utf-8", "utf-8"),
            )
        else:
            byte_data = b""
        _ = request_blocking.post(req, byte_data)
    else:
        err_msg = f"Request method {method} not supported."
        raise NetworkException(err_msg)

    reply: QgsNetworkReplyContent = request_blocking.reply()
    reply_error = reply.error()
    if reply_error != QNetworkReply.NoError:
        # Error content will be empty in older QGIS versions:
        # https://github.com/qgis/QGIS/issues/42442
        message = (
            bytes(reply.content()).decode("utf-8")
            if len(bytes(reply.content()))
            else None
        )
        # bar_msg will just show a generic Qt error string.
        raise NetworkException(
            message=message,
            error=reply_error,
            bar_msg=MessageBuilder.create_bar_message(reply.errorString()),
        )

    return bytes(reply.content())
