"""Message builder class for creating different QGIS message types."""

from enum import Enum

from qgis.core import Qgis
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface

from plugin.utilities.logger import get_plugin_logger
from plugin.utilities.resources import get_plugin_name

LOG = get_plugin_logger()


class MessageLevel(Enum):
    INFO = Qgis.MessageLevel.Info
    WARNING = Qgis.MessageLevel.Warning
    ERROR = Qgis.MessageLevel.Critical
    SUCCESS = Qgis.MessageLevel.Success


class MessageBuilder:
    """Message logger class for creating QGIS messages."""

    @staticmethod
    def create_bar_message(
        message: str,
        message_level: MessageLevel = MessageLevel.INFO,
        duration: int | None = None,
    ) -> None:
        """Create bar message that is displayed on top of the map.

        Args:
            message (str): _description_
            message_type (MessageTypes): _description_
            duration (int | None, optional): _description_. Defaults to 10.
        """
        # check if this is permanent and problem-related message
        if (
            duration is None
            and message_level in (MessageLevel.ERROR, MessageLevel.WARNING)
            and hasattr(iface.messageBar(), "clearWidgets")
        ):
            # adding permanent problem message means that we can remove
            # existing message bars since this supposedly is the only relevant
            # thing now
            iface.messageBar().clearWidgets()

        message_duration = duration
        if message_duration is None:
            message_duration = 10

        iface.messageBar().pushMessage(
            get_plugin_name(),
            message,
            level=message_level.value,
            duration=message_duration,
        )

    @staticmethod
    def create_window_message(
        title: str,
        message: str,
        buttons: QMessageBox.StandardButtons,
        info_text: str | None,
    ) -> int:
        """Create a window message that is shown as a seperate window.

        returnValue = MessageBuilder.createWindowMessage(
            title,
            msg,
            QMessageBox.Ok | QMessageBox.Cancel,
            info_text
        )

        if returnValue == QMessageBox.Ok:
            // Ok was clicked
        if returnValue == QMessageBox.Cancel:
            // Cancel was clicked

        See https://doc.qt.io/qt-5/qmessagebox.html#StandardButton-enum
        for more Button types

        Args:
            title (str): _description_
            message (str): _description_
            buttons (QMessageBox.StandardButtons): _description_
            info_text (str | None): _description_

        Returns:
            int: _description_
        """
        msg = QMessageBox()

        msg.setWindowTitle(title)
        msg.setText(message)

        if info_text:
            msg.setInformativeText(info_text)

        msg.setStandardButtons(buttons)

        return msg.exec_()

    @staticmethod
    def create_info_prompt(title: str, message: str) -> None:
        """Create simple info prompt.

        Args:
            title (str): _description_
            message (str): _description_
        """
        QMessageBox.information(
            iface.mainWindow(),
            title,
            message,
        )

    @staticmethod
    def create_yes_no_prompt(title: str, message: str) -> bool:
        """Create simple yes/no prompt.

        Args:
            title (str): _description_
            message (str): _description_

        Returns:
            bool: boolean based on given input.
        """
        answer = QMessageBox.question(
            iface.mainWindow(),
            title,
            message,
            QMessageBox.Yes,
            QMessageBox.No,
        )

        return answer == QMessageBox.Yes
