# Layer Opacity Control using shortcut keys for Krita

A Krita plugin that allows you to quickly increase or decrease the opacity of the active layer using keyboard shortcuts with configurable increments.

## ✨ Features

- **Quick Opacity Adjustment**: Increase or decrease layer opacity with a single click or keybind.
- **Configurable Increments**: Set your own opacity step value (e.g., 5, 10, 17) via a built-in settings dialog.
- **Auto-Shortcut Installation**: The plugin automatically installs its action definitions, making it easy to assign keyboard shortcuts.
- **Cross-Platform**: Works on Windows, Linux, and macOS.

## Why is this needed?

Maintaining high-speed momentum during digital painting relies on keeping your focus on the canvas and your hands on your shortcut keys. While adjusting canvas zoom, brush size, and brush opacity can be handled entirely via hotkeys, adjusting a layer's transparency currently requires navigating the cursor away from the drawing area to interact with the slider in the Layers docker.

This plugin bridges that workflow gap by allowing artists to map layer opacity adjustments directly to their keyboard. By minimizing repetitive cursor travel, it creates a smoother, more fluid painting experience and keeps your focus right where your stylus meets the canvas.

## Default Krita shortcut limitations for layer adjustments

Krita features an incredibly robust shortcut system, including default keys to quickly step your active brush preset's opacity up or down. However, a parallel hotkey action does not yet exist for individual layer nodes. 

* **Feature Parity:** While brush opacity relies on quick keyboard adjustments to shift values on the fly, layer opacity remains a purely mouse- or stylus-driven slider interaction. 
* **Layer Operations Context:** Krita provides deep keyboard control for managing the layer stack—allowing users to seamlessly create, delete, merge, or reorder layers via hotkeys—but layer properties like transparency do not yet share this native keyboard integration.


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
