# Layer Opacity Control (v2.0)

Krita Python plugin. Adjust active layer opacity via configurable percent increment.

## Install
1. Tools > Scripts > Import Python Plugin from File...
2. Select `layer_opacity_control.zip`
3. Restart Krita
4. Settings > Configure Krita > Python Plugin Manager > enable `Layer Opacity Control`
5. Restart Krita
6. Settings > Configure Krita > Keyboard Shortcuts > search `Layer Opacity Control` > assign keys

## Actions
- Increase Layer Opacity: `+increment`
- Decrease Layer Opacity: `-increment`
- Configure Opacity Increment: set `1..100`, default `7`

## Config
- Path: `<AppDataLocation>/layer_opacity_control/config.json`
- Key: `increment_percent`
- Range: `1..100`
- Default: `7`

## Behavior
- Clamps opacity `0..100%`
- Snaps to whole-percent before delta to avoid rounding drift
- Skips locked layers
- Pass-through groups: `setPassThrough(False)` before `setOpacity`
- Forces repaint via `setBlendingMode(node.blendingMode())`
- Does not call `refreshProjection()`

## Files
- `layer_opacity_control.desktop`
- `layer_opacity_control/`
  - `__init__.py`
  - `layer_opacity_control.py`
  - `layer_opacity_control.action`
  - `layer_opacity_control_manual.html`

## Troubleshooting
- Actions missing: enable plugin, restart Krita
- Shortcut does nothing: action file not installed, restart Krita
- No active layer: select layer
- Locked layer: unlock
- Group layer no effect: pass-through converted to Normal on opacity change
