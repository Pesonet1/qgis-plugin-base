from pathlib import Path

from qgis.core import (
    QgsProject,
    QgsRasterLayer,
)
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QDialog, QWidget
from qgis.utils import iface

from plugin.utilities.i18n import translate
from plugin.utilities.logger import get_plugin_logger
from plugin.utilities.message_builder import (
    MessageBuilder,
    MessageLevel,
)

LOG = get_plugin_logger()


class ExampleDialog(QDialog):
    layer_name = "OpenStreetMap"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        uic.loadUi(Path(__file__).parent / "example_dialog.ui", self)

        self.add_layer_button: QtWidgets.QPushButton
        self.remove_layer_button: QtWidgets.QPushButton

        self.add_layer_button.clicked.connect(self.add_layer_button_clicked)
        self.remove_layer_button.clicked.connect(
            self.remove_layer_button_clicked
        )

    def add_layer_button_clicked(self) -> None:
        LOG.info("add layer button clicked!")

        MessageBuilder.create_bar_message(
            translate("example", "addRasterLayer"), MessageLevel.INFO
        )

        osm = "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png&zmax=19&zmin=0"

        layer_to_add = QgsProject.instance().mapLayersByName(self.layer_name)
        if layer_to_add:
            return

        osm_layer = QgsRasterLayer(osm, self.layer_name, "wms")
        crs = osm_layer.crs()
        crs.createFromId(3067)
        osm_layer.setCrs(crs)

        if osm_layer.isValid():
            QgsProject.instance().addMapLayer(osm_layer)

    def remove_layer_button_clicked(self) -> None:
        LOG.info("remove layer button clicked!")

        layer_to_remove = QgsProject.instance().mapLayersByName(
            self.layer_name
        )
        if layer_to_remove:
            QgsProject.instance().removeMapLayer(layer_to_remove[0])

        iface.mapCanvas().refresh()
