from bpy.types import Panel, PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class

class FLATANA_PT_panel(Panel):
    bl_idname = 'FLATANA_PT_panel'
    bl_label = 'Flatana'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Flatana'

    def draw(self, context):
        # flatten op
        op = self.layout.operator('flatana.flatten', icon='ORIENTATION_NORMAL')
        op.mode = context.window_manager.flatana_vars.mode
        op.iterations = context.window_manager.flatana_vars.iterations
        op.strength = context.window_manager.flatana_vars.strength
        op.only_selected_faces = context.window_manager.flatana_vars.only_selected_faces
        # options
        self.layout.prop(context.window_manager.flatana_vars, 'mode')
        self.layout.prop(context.window_manager.flatana_vars, 'iterations')
        self.layout.prop(context.window_manager.flatana_vars, 'strength')
        self.layout.prop(context.window_manager.flatana_vars, 'only_selected_faces')


def register():
    register_class(FLATANA_PT_panel)


def unregister():
    unregister_class(FLATANA_PT_panel)
