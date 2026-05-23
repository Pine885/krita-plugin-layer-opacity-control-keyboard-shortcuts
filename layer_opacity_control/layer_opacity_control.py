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
            resources_dir = os.path.join(data_location, "krita")
            actions_dir = os.path.join(resources_dir, "actions")
            os.makedirs(actions_dir, exist_ok=True)

            # Source: the .action file shipped inside the plugin folder
            src = os.path.join(self.plugin_dir, self.action_file_name)
            dst = os.path.join(actions_dir, self.action_file_name)

            if not os.path.exists(dst):
                if os.path.exists(src):
                    shutil.copyfile(src, dst)
                    print(f"Layer Opacity Control: Keyboard shortcut file installed to {dst}. Please restart Krita to use it.")
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
                    return config.get("increment", self.default_increment)
        except Exception as e:
            print(f"Error reading config: {e}")
        return self.default_increment

    def set_increment(self, value):
        """Saves the opacity increment to the config file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({"increment": value}, f)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Could not save configuration: {e}")

    def increase_opacity(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            return

        node = doc.activeNode()
        if not node:
            return

        increment = self.get_increment()
        current_opacity = node.opacity()
        new_opacity = min(255, current_opacity + increment)
        
        node.setOpacity(new_opacity)
        # Force UI update
        node.setBlendingMode(node.blendingMode())

    def decrease_opacity(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            return

        node = doc.activeNode()
        if not node:
            return

        increment = self.get_increment()
        current_opacity = node.opacity()
        new_opacity = max(0, current_opacity - increment)
        
        node.setOpacity(new_opacity)
        # Force UI update
        node.setBlendingMode(node.blendingMode())

    def configure_opacity(self):
        current_val = self.get_increment()
        new_val, ok = QInputDialog.getInt(
            None, 
            "Configure Opacity Control", 
            "Opacity Increment (0-255):", 
            value=current_val, 
            min=1, 
            max=255
        )
        
        if ok:
            self.set_increment(new_val)
