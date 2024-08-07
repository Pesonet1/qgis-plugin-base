import os
from collections.abc import Callable

from qgis.PyQt.QtCore import (
    QCoreApplication,
    QTranslator,
)
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QWidget
from qgis.utils import iface

from plugin.ui.example_dialog import ExampleDialog
from plugin.utilities.i18n import setup_translations
from plugin.utilities.logger import (
    get_plugin_logger,
    init_logger,
    remove_logger,
)
from plugin.utilities.resources import (
    get_plugin_name,
    get_resource_path,
)

LOG = get_plugin_logger()


class Plugin:
    """QGIS Plugin Implementation."""

    def __init__(self) -> None:
        init_logger(get_plugin_name())

        plugin_dir = os.path.dirname(__file__)

        translation_file_path = setup_translations(plugin_dir)
        if translation_file_path:
            self.translator = QTranslator()
            self.translator.load(translation_file_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions: list[QAction] = []
        self.menu = get_plugin_name()

    def add_action(
        self,
        icon_path: str,
        text: str,
        name: str,
        callback: Callable,
        *,
        enabled_flag: bool = True,
        add_to_menu: bool = True,
        add_to_toolbar: bool = True,
        status_tip: str | None = None,
        whats_this: str | None = None,
        parent: QWidget | None = None,
    ) -> QAction:
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.

        :param text: Text that should be shown in menu items for this action.

        :param callback: Function to be called when the action is triggered.

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.

        :param parent: Parent widget for the new action. Defaults None.

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.setObjectName(name)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            iface.addToolBarIcon(action)

        if add_to_menu:
            iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self) -> None:
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.toolbar = iface.addToolBar(get_plugin_name())
        self.toolbar.setObjectName(get_plugin_name())

        action_icon = str(get_resource_path("icons/dog.png"))

        self.toolbar.addAction(
            self.add_action(
                action_icon,
                text=get_plugin_name(),
                name="showExampleDialog",
                callback=self.run,
                parent=iface.mainWindow(),
                add_to_toolbar=False,
                add_to_menu=False,
            )
        )

    def onClosePlugin(self) -> None:
        """Cleanup necessary items here when plugin dockwidget is closed"""

    def unload(self) -> None:
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            iface.removePluginMenu(get_plugin_name(), action)
            iface.removeToolBarIcon(action)
            iface.unregisterMainWindowAction(action)

        remove_logger(get_plugin_name())

    def run(self) -> None:
        """Run method that performs all the real work"""

        ExampleDialog(parent=iface.mainWindow()).exec()
