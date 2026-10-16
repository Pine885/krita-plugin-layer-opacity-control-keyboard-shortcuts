from krita import Krita
from .layer_opacity_control import LayerOpacityExtension

try:
    Krita.instance().addExtension(LayerOpacityExtension(Krita.instance()))
except Exception as e:
    print(f"Layer Opacity Control: failed to register extension: {e}")
