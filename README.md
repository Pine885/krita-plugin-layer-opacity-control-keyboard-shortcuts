# Layer Opacity Control using shortcut keys for Krita

A Krita plugin that allows you to quickly increase or decrease the opacity of the active layer using keyboard shortcuts with configurable increments.

## ✨ Features

- **Quick Opacity Adjustment**: Increase or decrease layer opacity with a single click or keybind.
- **Configurable Increments**: Set your own opacity step value (e.g., 5, 10, 17) via a built-in settings dialog.
- **Auto-Shortcut Installation**: The plugin automatically installs its action definitions, making it easy to assign keyboard shortcuts.
- **Cross-Platform**: Works on Windows, Linux, and macOS.

## 🚀 Installation

### 1. Import the Plugin
1. Download the latest release ZIP file.
2. In Krita, go to **Tools** ‣ **Scripts** ‣ **Import Python Plugin from File…**
3. Select the downloaded ZIP file.

### 2. Enable the Plugin
1. Restart **Krita**.
2. Go to **Settings** ‣ **Configure Krita**.
3. Select **Python Plugin Manager** from the left sidebar.
4. Find **Layer Opacity Control** in the list and check the box next to it.
5. Click **OK**.
6. **Restart Krita** one more time.

### 3. Finalize Shortcuts
The plugin automatically copies its shortcut definitions to the Krita resources folder on its first run. To make these shortcuts available in the settings menu:
1. **Restart Krita one last time**.

## 🛠️ Usage

### Accessing the Plugin
You can find the plugin actions under the menu:
**Tools** ‣ **Scripts** ‣ **Layer Opacity Control**
- **Increase Layer Opacity**: Increases opacity by the set increment.
- **Decrease Layer Opacity**: Decreases opacity by the set increment.
- **Configure Opacity Increment**: Opens a dialog to change the increment value.

### Setting Keyboard Shortcuts
1. Go to **Settings** ‣ **Configure Krita**.
2. Select **Keyboard Shortcuts**.
3. Search for **"Layer Opacity Control"**.
4. Assign your preferred keys to the increase and decrease actions.

## 📜 License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
