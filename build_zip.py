#!/usr/bin/env python3
"""Rebuild layer_opacity_control.zip from the plugin source tree.

Krita's "Import Python Plugin from File..." logic lives in
``plugins/python/plugin_importer/plugin_importer.py``. It finds a plugin by:

1. locating a ``<name>.desktop`` file, reading ``X-KDE-Library`` for ``name``;
2. looking for an archive entry equal to ``<name>/`` (or ending in ``/<name>/``)
   that also contains ``<name>/__init__.py``.

Step 2 requires an explicit *directory* entry. Python's ``zipfile`` only writes
file entries by default, so directory entries must be added on purpose; without
them Krita reports "No plugins found in archive".

Usage:
    python3 build_zip.py
"""

import configparser
import os
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
PLUGIN_DIR = os.path.join(ROOT, "layer_opacity_control")
ZIP_PATH = os.path.join(ROOT, "layer_opacity_control.zip")

EXCLUDED_DIRS = {"__pycache__"}
EXCLUDED_FILES = {"config.json"}


def _iter_entries():
    """Yield (filesystem_path, archive_name) pairs, including directory entries."""
    for dirpath, dirnames, filenames in os.walk(PLUGIN_DIR):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDED_DIRS)

        # Directory entry. The plugin root is skipped so its contents sit at the
        # zip root (matching Krita's expected layout); nested directories such as
        # the module folder MUST be written as explicit entries.
        if dirpath != PLUGIN_DIR:
            yield dirpath, os.path.relpath(dirpath, PLUGIN_DIR)

        for name in sorted(filenames):
            if name in EXCLUDED_FILES or name.endswith((".pyc", ".pyo")):
                continue
            full_path = os.path.join(dirpath, name)
            yield full_path, os.path.relpath(full_path, PLUGIN_DIR)


def _verify(zip_path):
    """Re-run Krita's plugin detection logic against the built archive."""
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        desktops = [n for n in names if n.endswith(".desktop")]
        if not desktops:
            raise SystemExit("verification failed: no .desktop file in archive")

        for desktop in desktops:
            config = configparser.ConfigParser()
            config.read_string(archive.read(desktop).decode("utf-8"))
            module = config["Desktop Entry"]["X-KDE-Library"]
            if module + "/" not in names:
                raise SystemExit(
                    "verification failed: missing directory entry '%s/' "
                    "(Krita's importer requires it)" % module
                )
            if "%s/__init__.py" % module not in names:
                raise SystemExit(
                    "verification failed: missing '%s/__init__.py'" % module
                )


def build():
    if not os.path.isdir(PLUGIN_DIR):
        raise SystemExit("Plugin directory not found: %s" % PLUGIN_DIR)

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    count = 0
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for full_path, arcname in _iter_entries():
            archive.write(full_path, arcname)
            count += 1

    _verify(ZIP_PATH)
    print("Wrote %s (%d entries)" % (ZIP_PATH, count))


if __name__ == "__main__":
    build()
