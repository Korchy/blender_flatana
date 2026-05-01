if "bpy" in locals():
    import importlib
    importlib.reload(flatana_vars)
    importlib.reload(flatana_ops)
    importlib.reload(flatana_panel)
else:
    from . import flatana_vars
    from . import flatana_ops
    from . import flatana_panel

bl_info = {
    'name': 'Flatana',
    'category': 'Mesh',
    'version': (1, 0, 0),
    'blender': (5, 1, 0),
}

def register():
    flatana_vars.register()
    flatana_ops.register()
    flatana_panel.register()


def unregister():
    flatana_panel.unregister()
    flatana_ops.unregister()
    flatana_vars.unregister()


if __name__ == '__main__':
    register()
