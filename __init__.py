# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the License Zero Parity 7.0.0 (see LICENSE-PARITY file) and MIT (contributions, see LICENSE-MIT file) with exception License Zero Patron 1.0.0 (see LICENSE-PATRON file)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


bl_info = {
    "name": "TextMeshCreator",
    "author": "Natsuneko",
    "description": "Blender add-on for creating 3D Text Objects from strings",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
    "location": "3D View > Sidebar > TextMesh Creator",
    "warning": "",
    "category": "Generic"
}

if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(properties)
    importlib.reload(ui)
    importlib.reload(utils)
    importlib.reload(wrapper)
else:
    from . import operator
    from . import properties
    from . import ui
    from . import utils
    from . import wrapper

    import bpy
    from bpy.props import PointerProperty


classes = [
    operator.TextMeshCreatorOperation,
    properties.TextMeshCreatorProperties,
    ui.TextMeshCreatorUI
]


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.TextMeshCreatorProperties = PointerProperty(type=properties.TextMeshCreatorProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.TextMeshCreatorProperties


if __name__ == "__main__":
    register()
