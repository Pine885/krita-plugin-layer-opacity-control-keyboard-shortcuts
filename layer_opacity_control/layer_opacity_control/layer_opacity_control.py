from krita import Extension, Krita
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
    QSpinBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStandardPaths
import filecmp
import json
import os
import shutil
import tempfile

from .opacity_math import compute_new_opacity, legacy_units_to_percent

PLUGIN_VERSION = "2.1.0"


class OptionsDialog(QDialog):
    """Small options dialog: opacity increment and multi-layer behaviour."""

    def __init__(self, parent, increment, apply_all_layers):
        super().__init__(parent)
        self.setWindowTitle("Layer Opacity Control")

        layout = QFormLayout(self)

        self.increment_spin = QSpinBox(self)
        self.increment_spin.setRange(1, 100)
        self.increment_spin.setValue(increment)
        self.increment_spin.setSuffix(" %")
        layout.addRow("Opacity increment:", self.increment_spin)

        self.apply_all_check = QCheckBox("Apply to all selected layers", self)
        self.apply_all_check.setChecked(apply_all_layers)
        layout.addRow("", self.apply_all_check)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def values(self):
        return self.increment_spin.value(), self.apply_all_check.isChecked()


class LayerOpacityExtension(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.plugin_dir = os.path.dirname(__file__)
        self.action_file_name = "layer_opacity_control.action"
        self.default_increment_percent = 5   # percent; legacy scripts used 17/255 (=7%)
        self.default_apply_all_layers = False
        self.config_file = self._get_config_file()
        self._config = None

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

            # Compare contents rather than timestamps: unzipping resets mtimes
            # and clock skew would otherwise skip legitimate updates.
            if not os.path.exists(dst) or not filecmp.cmp(src, dst, shallow=False):
                shutil.copyfile(src, dst)
                print(
                    f"Layer Opacity Control: installed/updated action file to {dst}. "
                    "Restart Krita for shortcuts to appear."
                )
        except Exception as e:
            print(f"Layer Opacity Control: could not install .action file: {e}")

    # -- configuration ----------------------------------------------------

    def _load_config(self):
        if self._config is not None:
            return self._config

        config = {}
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f) or {}
        except Exception as e:
            print(f"Layer Opacity Control: error reading config: {e}")
            config = {}

        # Migrate the pre-2.0 unit-based config (1..255) to percent.
        if "increment_percent" not in config and "increment" in config:
            try:
                config["increment_percent"] = legacy_units_to_percent(config["increment"])
            except Exception as e:
                print(f"Layer Opacity Control: could not migrate legacy increment: {e}")

        self._config = config
        return config

    def get_increment_percent(self):
        raw = self._load_config().get("increment_percent", self.default_increment_percent)
        try:
            return max(1, min(100, int(raw)))
        except (TypeError, ValueError):
            return self.default_increment_percent

    def get_apply_all_layers(self):
        return bool(self._load_config().get("all_selected_layers", self.default_apply_all_layers))

    def set_increment_percent(self, value):
        self._save_config(increment_percent=max(1, min(100, int(value))))

    def set_apply_all_layers(self, value):
        self._save_config(all_selected_layers=bool(value))

    def _save_config(self, **changes):
        config = dict(self._load_config())
        config.pop("increment", None)  # legacy key no longer needed
        config.update(changes)
        try:
            self._write_config(config)
        except Exception as e:
            QMessageBox.critical(
                self._parent_window(),
                "Layer Opacity Control",
                f"Could not save configuration:\n{e}"
            )
            return
        self._config = config

    def _write_config(self, data):
        config_dir = os.path.dirname(self.config_file) or "."
        os.makedirs(config_dir, exist_ok=True)
        # Write to a temp file first, then swap it in, so a crash mid-write
        # cannot leave a half-written (corrupt) config behind.
        fd, tmp_path = tempfile.mkstemp(prefix=".config-", suffix=".json", dir=config_dir)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp_path, self.config_file)
        except Exception:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except OSError:
                pass
            raise

    # -- window helpers ---------------------------------------------------

    def _parent_window(self):
        try:
            return Krita.instance().activeWindow().qwindow()
        except Exception:
            return None

    def _active_view(self):
        try:
            window = Krita.instance().activeWindow()
            return window.activeView() if window else None
        except Exception:
            return None

    def _notify(self, message):
        view = self._active_view()
        try:
            if view is not None:
                view.showFloatingMessage(message, QIcon(), 2000, 0)
                return
        except Exception:
            pass
        print(f"Layer Opacity Control: {message}")

    # -- opacity ----------------------------------------------------------

    def _target_nodes(self, doc):
        if self.get_apply_all_layers():
            view = self._active_view()
            if view is not None:
                try:
                    nodes = list(view.selectedNodes())
                    if nodes:
                        return nodes
                except Exception as e:
                    print(f"Layer Opacity Control: could not read selected layers: {e}")
        node = doc.activeNode()
        return [node] if node else []

    @staticmethod
    def _is_locked(node):
        try:
            locked = getattr(node, "locked", None)
            return bool(locked()) if callable(locked) else False
        except Exception:
            return False

    @staticmethod
    def _apply_opacity(node, opacity):
        node.setOpacity(opacity)
        # Force a repaint. refreshProjection() is intentionally not used.
        node.setBlendingMode(node.blendingMode())

    def _modify_opacity(self, delta):
        try:
            self._modify_opacity_impl(delta)
        except Exception as e:
            print(f"Layer Opacity Control: error changing opacity: {e}")
            self._notify("Layer Opacity Control: error, see console.")

    def _modify_opacity_impl(self, delta):
        doc = Krita.instance().activeDocument()
        if not doc:
            self._notify("Layer Opacity Control: no active document.")
            return

        nodes = self._target_nodes(doc)
        if not nodes:
            self._notify("Layer Opacity Control: no active layer.")
            return

        increment_percent = self.get_increment_percent()
        changed = 0
        locked = 0

        for node in nodes:
            if self._is_locked(node):
                locked += 1
                continue
            try:
                current_opacity = node.opacity()
                new_opacity = compute_new_opacity(current_opacity, delta, increment_percent)
                if new_opacity == current_opacity:
                    continue
                self._apply_opacity(node, new_opacity)
                changed += 1
            except Exception as e:
                print(f"Layer Opacity Control: could not adjust layer: {e}")

        if changed == 0 and locked:
            self._notify("Layer Opacity Control: layer is locked.")
        elif changed > 1:
            self._notify(f"Layer Opacity Control: adjusted {changed} layers.")

    def increase_opacity(self):
        self._modify_opacity(1)

    def decrease_opacity(self):
        self._modify_opacity(-1)

    def configure_opacity(self):
        dialog = OptionsDialog(
            self._parent_window(),
            self.get_increment_percent(),
            self.get_apply_all_layers(),
        )
        if dialog.exec_() == QDialog.Accepted:
            increment, apply_all = dialog.values()
            self.set_increment_percent(increment)
            self.set_apply_all_layers(apply_all)
