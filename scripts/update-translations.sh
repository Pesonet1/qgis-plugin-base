#!/usr/bin/env bash

echo "Updating translations"

# get path to the plugin directory (while resolving symlinks)
PLUGIN_DIR=$(dirname $(dirname $(realpath $0)))

echo "Updating .ts files"
# first update the .ts files with new possible translations
pylupdate5 -verbose $PLUGIN_DIR/translations.pro

echo "Compiling translations"

# first check if the lrelease is available under lrelease-qt5 command
# there might be problems with the pypi version of the qt5-tools packed lrelease
# so try other options first
if command -v lrelease-qt5 &>/dev/null; then
    lrelease-qt5 $PLUGIN_DIR/plugin/resources/i18n/fi.ts -qm $PLUGIN_DIR/plugin/resources/i18n/fi.qm
else
    qt5-tools lrelease $PLUGIN_DIR/plugin/resources/i18n/fi.ts -qm $PLUGIN_DIR/plugin/resources/i18n/fi.qm
fi
