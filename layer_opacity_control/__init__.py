from .layer_opacity_control import LayerOpacityExtension

# Register the extension with Krita when the plugin is loaded
Krita.instance().addExtension(LayerOpacityExtension(Krita.instance()))
