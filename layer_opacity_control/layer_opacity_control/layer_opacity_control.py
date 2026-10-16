from krita import Extension, Krita
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths
import os
import json
import shutil


class LayerOpacityExtension(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.plugin_dir = os.path.dirname(__file__)
        self.action_file_name = "layer_opacity_control.action"
        self.default_increment_percent = 5   # ≈ old 17/255
        self.config_file = self._get_config_file()

    def _get_config_file(self):
        try:
            data_location = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            if data_location:
                config_dir = os.path.join(data_location, "layer_opacity_control")
                os.makedirs(config_dir, exist_ok=True)
                return os.path.join(config_dir, "config.json")
        except Exception as e:
            print(f"Layer Opacity Control: AppDataLocation unavailable, using plugin dir: {e}")
        return os.path.join(self.plugin_dir, "config.json")

    def setup(self):
        self.install_action_file()

    def createActions(self, window):
        self.action_increase = window.createAction(
            "layer_opacity_increase",
            "Increase Layer Opacity",
            "tools/scripts"
        )
        self.action_increase.triggered.connect(self.increase_opacity)

        self.action_decrease = window.createAction(
            "layer_opacity_decrease",
            "Decrease Layer Opacity",
            "tools/scripts"
        )
        self.action_decrease.triggered.connect(self.decrease_opacity)

        self.action_configure = window.createAction(
            "layer_opacity_configure",
            "Configure Opacity Increment",
            "tools/scripts"
        )
        self.action_configure.triggered.connect(self.configure_opacity)

    def install_action_file(self):
        try:
            data_location = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            if not data_location:
                return

            actions_dir = os.path.join(data_location, "actions")
            os.makedirs(actions_dir, exist_ok=True)

            src = os.path.join(self.plugin_dir, self.action_file_name)
            dst = os.path.join(actions_dir, self.action_file_name)

            if not os.path.exists(src):
                print(f"Layer Opacity Control: source action file missing: {src}")
                return

            if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copyfile(src, dst)
                print(
                    f"Layer Opacity Control: installed/updated action file to {dst}. "
                    "Restart Krita for shortcuts to appear."
                )
        except Exception as e:
            print(f"Layer Opacity Control: could not install .action file: {e}")

    def get_increment_percent(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)

                if "increment_percent" in config:
                    return max(1, min(100, int(config["increment_percent"])))

                # migrate old unit-based config
                if "increment" in config:
                    old_units = max(1, min(255, int(config["increment"])))
                    return max(1, min(100, round(old_units * 100 / 255)))

        except Exception as e:
            print(f"Layer Opacity Control: error reading config: {e}")

        return self.default_increment_percent

    def set_increment_percent(self, value):
        try:
            val = max(1, min(100, int(value)))
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump({"increment_percent": val}, f, indent=2)
        except Exception as e:
            QMessageBox.critical(
                self._parent_window(),
                "Layer Opacity Control",
                f"Could not save configuration:\n{e}"
            )

    def _parent_window(self):
        try:
            return Krita.instance().activeWindow().qwindow()
        except Exception:
            return None

    def _modify_opacity(self, delta):
        doc = Krita.instance().activeDocument()
        if not doc:
            return

        node = doc.activeNode()
        if not node:
            return

        if hasattr(node, "locked") and node.locked():
            return

        increment_percent = self.get_increment_percent()

        current_opacity = node.opacity()

        # Snap to Krita's displayed whole-percent value first.
        # This prevents rounding drift across repeated presses.
        current_percent = round(current_opacity * 100.0 / 255.0)

        new_percent = max(
            0,
            min(100, current_percent + (delta * increment_percent))
        )
        new_opacity = int(round(new_percent * 255.0 / 100.0))

        if new_opacity == current_opacity:
            return

        if (
            node.type() == "grouplayer"
            and hasattr(node, "passThrough")
            and hasattr(node, "setPassThrough")
            and node.passThrough()
        ):
            node.setPassThrough(False)

        node.setOpacity(new_opacity)
        node.setBlendingMode(node.blendingMode())

    def increase_opacity(self):
        self._modify_opacity(1)

    def decrease_opacity(self):
        self._modify_opacity(-1)

    def configure_opacity(self):
        current_val = self.get_increment_percent()
        new_val, ok = QInputDialog.getInt(
            self._parent_window(),
            "Configure Opacity Control",
            "Opacity Increment (%):",
            value=current_val,
            min=1,
            max=100
        )
        if ok:
            self.set_increment_percent(new_val)
