from krita import *
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5.QtCore import QStandardPaths
import os
import json
import shutil

class LayerOpacityExtension(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.plugin_dir = os.path.dirname(__file__)
        try:
            data_location = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            config_dir = os.path.join(data_location, "layer_opacity_control")
            os.makedirs(config_dir, exist_ok=True)
            self.config_file = os.path.join(config_dir, "config.json")
        except Exception as e:
            print(f"Layer Opacity Control: Could not use AppDataLocation for config, falling back to plugin directory: {e}")
            self.config_file = os.path.join(self.plugin_dir, "config.json")
        self.action_file_name = "layer_opacity_control.action"
        self.default_increment = 17

    def setup(self):
        # Install the .action file on first run for automatic shortcut registration
        self.install_action_file()

    def createActions(self, window):
        # Create actions in the Tools -> Scripts menu
        self.action_increase = window.createAction("layer_opacity_increase", "Increase Layer Opacity", "tools/scripts")
        self.action_increase.triggered.connect(self.increase_opacity)

        self.action_decrease = window.createAction("layer_opacity_decrease", "Decrease Layer Opacity", "tools/scripts")
        self.action_decrease.triggered.connect(self.decrease_opacity)

        self.action_configure = window.createAction("layer_opacity_configure", "Configure Opacity Increment", "tools/scripts")
        self.action_configure.triggered.connect(self.configure_opacity)

    def install_action_file(self):
        """Copies the .action file to the Krita resources directory automatically."""
        try:
            # Determine the writable Krita resources directory
            data_location = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
            resources_dir = data_location
            actions_dir = os.path.join(resources_dir, "actions")
            os.makedirs(actions_dir, exist_ok=True)

            # Source: the .action file shipped inside the plugin folder
            src = os.path.join(self.plugin_dir, self.action_file_name)
            dst = os.path.join(actions_dir, self.action_file_name)

            if not os.path.exists(dst) or (os.path.exists(src) and os.path.getmtime(src) > os.path.getmtime(dst)):
                if os.path.exists(src):
                    shutil.copyfile(src, dst)
                    print(f"Layer Opacity Control: Keyboard shortcut file installed/updated to {dst}. Please restart Krita to use it.")
                else:
                    print(f"Layer Opacity Control: Source action file not found at {src}")
        except Exception as e:
            print(f"Layer Opacity Control: Could not install .action file: {e}")

    def get_increment(self):
        """Reads the opacity increment from the config file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    val = int(config.get("increment", self.default_increment))
                    return max(1, min(255, val))
        except Exception as e:
            print(f"Error reading config: {e}")
        return self.default_increment

    def set_increment(self, value):
        """Saves the opacity increment to the config file."""
        try:
            val = int(value)
            val = max(1, min(255, val))
            with open(self.config_file, 'w') as f:
                json.dump({"increment": val}, f)
        except Exception as e:
            parent = None
            try:
                parent = Krita.instance().activeWindow().qwindow()
            except Exception:
                pass
            QMessageBox.critical(parent, "Error", f"Could not save configuration: {e}")

    def _modify_opacity(self, delta):
        doc = Krita.instance().activeDocument()
        if not doc:
            return

        node = doc.activeNode()
        if not node:
            return

        increment = self.get_increment()
        current_opacity = node.opacity()
        new_opacity = max(0, min(255, current_opacity + (delta * increment)))
        
        # If it's a group layer, ensure it's not a pass-through group so opacity is visible, but only if opacity changes
        if new_opacity != current_opacity and node.type() == 'grouplayer' and hasattr(node, 'passThrough') and node.passThrough():
            node.setPassThrough(False)

        node.setOpacity(new_opacity)
        # Force UI update
        node.setBlendingMode(node.blendingMode())

    def increase_opacity(self):
        self._modify_opacity(1)

    def decrease_opacity(self):
        self._modify_opacity(-1)

    def configure_opacity(self):
        current_val = self.get_increment()
        parent = None
        try:
            parent = Krita.instance().activeWindow().qwindow()
        except Exception:
            pass
        new_val, ok = QInputDialog.getInt(
            parent, 
            "Configure Opacity Control", 
            "Opacity Increment (1-255):", 
            value=current_val, 
            min=1, 
            max=255
        )
        
        if ok:
            self.set_increment(new_val)
