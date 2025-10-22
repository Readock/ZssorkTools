#!/bin/bash

PLUGIN_NAME="ZssorkTools"
KRITA_DIR="$HOME/.var/app/org.kde.krita/data/krita"  # (flatpak path)

echo "checking if exists: $KRITA_DIR/pykrita/$PLUGIN_NAME"
# Remove any old version
if [ -d "$KRITA_DIR/pykrita/$PLUGIN_NAME" ]; then
  echo "Removing old plugin version..."
  rm -rf "$KRITA_DIR/pykrita/$PLUGIN_NAME"
  rm "$KRITA_DIR/pykrita/$PLUGIN_NAME.desktop"
  rm "$KRITA_DIR/actions/$PLUGIN_NAME.action"
fi

# Copy over the plugin files
echo "Copying plugin files..."
cp -r "./$PLUGIN_NAME" "$KRITA_DIR/pykrita/$PLUGIN_NAME"
cp "./$PLUGIN_NAME.desktop" "$KRITA_DIR/pykrita/$PLUGIN_NAME.desktop"
cp "./$PLUGIN_NAME.action" "$KRITA_DIR/actions/$PLUGIN_NAME.action"

# run krita
flatpak run org.kde.krita