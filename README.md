# Layer Opacity Control v2.1.0

Krita Python plugin. Active-layer opacity +/- configurable percent.

## Install
1. Tools > Scripts > Import Python Plugin from File... -> `layer_opacity_control.zip`
2. Restart Krita
3. Settings > Configure Krita > Python Plugin Manager -> enable `Layer Opacity Control`
4. Restart Krita
5. Settings > Configure Krita > Keyboard Shortcuts -> search `Layer Opacity Control` -> assign keys

## Actions
| Action | Effect |
|---|---|
| Increase Layer Opacity | `+increment` |
| Decrease Layer Opacity | `-increment` |
| Configure Opacity Increment | dialog: increment + `all_selected_layers` |

## Config
- Path: `<AppDataLocation>/layer_opacity_control/config.json`

| Key | Type | Range/Values | Default |
|---|---|---|---|
| `increment_percent` | int | `1..100` | `5` |
| `all_selected_layers` | bool | `true`/`false` | `false` |

- Legacy `increment` (1..255) -> `increment_percent` on first read.
- Cache: in memory.
- Write: atomic (temp file + `os.replace`).

## Behavior
| Item | Value |
|---|---|
| Opacity clamp | `0..100%` |
| Percent snap | whole percent before delta |
| Locked layers | skipped |
| Multi-layer | `all_selected_layers=true` -> `View.selectedNodes()`; fallback `activeNode()` |
| Repaint | `setBlendingMode(node.blendingMode())` |
| No active layer / error | `View.showFloatingMessage()` |

## Files
- `layer_opacity_control.desktop`
- `layer_opacity_control/`
  - `__init__.py`
  - `layer_opacity_control.py`
  - `opacity_math.py`
  - `layer_opacity_control.action`
  - `layer_opacity_control_manual.html`
- `build_zip.py`
- `tests/test_opacity_math.py`

## Commands
| Task | Command |
|---|---|
| Rebuild zip | `python3 build_zip.py` |
| Run tests | `python3 -m unittest discover -s tests` |

## Troubleshooting
| Symptom | Fix |
|---|---|
| Actions missing | enable plugin, restart Krita |
| Shortcut does nothing | action file not installed, restart Krita |
| No active layer | select layer |
| Locked layer | unlock |
| Group layer no effect | check the group's pass-through and blend settings |
