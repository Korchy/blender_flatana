from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .flatana import Flatana

class FLATANA_OT_flatten(Operator):
    bl_idname = 'flatana.flatten'
    bl_label = 'Flatten'
    bl_description = 'Flatana - flatten faces'
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(     # noqa
        name='Mode',
        items=[
            ('AVERAGED', 'Averaged', 'Averaged', 0),
            ('SEQUENTIAL', 'Sequential', 'Sequential', 1)
        ],
        default='AVERAGED'
    )

    iterations: IntProperty(     # noqa
        name='Iterations',
        default=100,
        min=0
    )

    strength: FloatProperty(     # noqa
        name='Strength',
        default=3.5,
        min=0.0
    )

    only_selected_faces: BoolProperty(     # noqa
        name='Only selected faces',
        default=False
    )

    def execute(self, context):
        # flatten
        Flatana.flatten(
            obj=context.active_object,
            mode=self.mode,
            iterations=self.iterations,
            strength=self.strength,
            only_selected_faces=self.only_selected_faces
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH'


def register():
    register_class(FLATANA_OT_flatten)


def unregister():
    unregister_class(FLATANA_OT_flatten)
