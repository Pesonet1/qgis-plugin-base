import os

from qgis.PyQt.QtCore import QCoreApplication, QSettings

DEFAULT_LOCALE = "fi"


def setup_translations(plugin_dir_path: str) -> str:
    """Return QGIS locale and compiled translation file path for locale

    Args:
        plugin_dir_path (str): directory path to plugin source files

    Raises:
        FileNotFoundError: raised if locale file cannot be found

    Returns:
        str: translation .qm-file path
    """
    locale = QSettings().value("locale/userLocale")[0:2]
    if locale not in ["fi"]:
        locale = DEFAULT_LOCALE

    locale_path = os.path.join(
        plugin_dir_path, "resources", "i18n", f"{format(locale)}.qm"
    )

    if not os.path.exists(locale_path):
        raise FileNotFoundError(locale_path)

    return locale_path


def translate(
    context: str,
    text: str,
) -> str:
    """Get the translation for a string using Qt translation API.

    Args:
        context (str): Context of the translation e.g. class name etc.
        text (str): String for translation.

    Returns:
        str: Translated version of message
    """
    # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    return QCoreApplication.translate(context, text)
