from plugin.utilities.resources import get_plugin_name


def test_plugin_name() -> None:
    assert get_plugin_name() == "plugin"
