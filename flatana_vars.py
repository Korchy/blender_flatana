from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class


class FlatanaVars(PropertyGroup):

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
        default=0.3,
        min=0.0
    )

    only_selected_faces: BoolProperty(     # noqa
        name='Only selected faces',
        default=False
    )


def register():
    register_class(FlatanaVars)
    WindowManager.flatana_vars = PointerProperty(type=FlatanaVars)

def unregister():
    del WindowManager.flatana_vars
    unregister_class(FlatanaVars)
