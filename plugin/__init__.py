def classFactory(_):
    """Load plugin class from file plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from plugin.plugin import Plugin

    return Plugin()
