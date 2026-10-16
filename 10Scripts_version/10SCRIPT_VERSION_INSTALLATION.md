# Ten Scripts — Opacity Shortcuts

Prerequisite: Enable **Ten Scripts** in **Settings → Configure Krita → Python Plugin Manager**. Restart Krita.

## Files

### `increase_opacity.py`
```python
doc = Krita.instance().activeDocument()
node = doc.activeNode()
opacity = node.opacity()
node.setOpacity(min(255, opacity + 17))
node.setBlendingMode(node.blendingMode())
```

### `lower_opacity.py`
```python
doc = Krita.instance().activeDocument()
node = doc.activeNode()
opacity = node.opacity()
node.setOpacity(max(0, opacity - 17))
node.setBlendingMode(node.blendingMode())
```

## Increment
| Unit | Value | Percent |
|---|---:|---:|
| Krita opacity | 17 / 255 | ≈ 6.7% |

## Install
1. Create `increase_opacity.py` and `lower_opacity.py`.
2. Krita → **Tools** → **Scripts** → **Ten Scripts**.
3. Slot 1 → folder icon → `increase_opacity.py`.
4. Slot 2 → folder icon → `lower_opacity.py`.
5. Krita → **Settings** → **Configure Krita** → **Keyboard Shortcuts**.
6. Search `Ten Scripts`.
7. Bind **Slot 1** and **Slot 2**.

## Required Repaint Call
```python
node.setBlendingMode(node.blendingMode())
```
Do not remove. It forces canvas repaint.

## Troubleshooting
| Symptom | Fix |
|---|---|
| No Ten Scripts under Tools → Scripts | Enable plugin, restart Krita |
| Shortcut does nothing | Slot empty or file moved — re-pick file |
| No active layer | Select layer or unlock layer |
| Canvas does not repaint | Restore `setBlendingMode` line |
| Opacity stuck at 0 / 255 | Clamp reached — expected |
| Key conflict | Reassign in Keyboard Shortcuts |
| Group layer does nothing | Pass-through groups ignore own opacity — convert to Normal first |

## Limits vs Full Plugin
| Feature | Ten Scripts Version | Full Plugin |
|---|---|---|
| Increment | Hardcoded `17` | Configurable `1–100%` |
| Rapid-press acceleration | No | No |
| Pass-through group handling | No | Yes |
| Shortcut installation | Manual | `.action` file |
| Config persistence | No | JSON |
