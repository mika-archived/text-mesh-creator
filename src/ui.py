# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

from bpy.types import Panel

from .operator import TextMeshCreatorOperation
from .properties import TextMeshCreatorProperties


class TextMeshCreatorUI(Panel):
    bl_idname = "UI_PT_TextMeshCreator"
    bl_label = "TextMesh Creator Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "TestMesh Creator"

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        column.use_property_split = True

        props: TextMeshCreatorProperties = context.scene.TextMeshCreatorProperties

        column.label(text="Generic")
        column.prop(props, "strings")
        column.prop(props, "rotation_x")
        column.prop(props, "rotation_y")
        column.prop(props, "rotation_z")
        column.prop(props, "scale_x")
        column.prop(props, "scale_y")
        column.prop(props, "scale_z")
        column.prop(props, "font_path")
        column.prop(props, "separate_by")

        column.separator()
        column.label(text="Text Layout")
        column.prop(props, "thickness")
        column.prop(props, "horizontal_alignment")
        column.prop(props, "vertical_alignment")
        column.prop(props, "character_spacing")
        column.prop(props, "word_spacing")

        column.separator()
        column.label(text="Blendshape")
        column.prop(props, "use_blendshape")

        col_blendshape = column.column()
        col_blendshape.enabled = props.use_blendshape
        col_blendshape.prop(props, "blendshape_min_x")
        col_blendshape.prop(props, "blendshape_max_x")
        col_blendshape.prop(props, "blendshape_min_y")
        col_blendshape.prop(props, "blendshape_max_y")
        col_blendshape.prop(props, "blendshape_min_z")
        col_blendshape.prop(props, "blendshape_max_z")

        column.separator()
        column.label(text="Mesh")
        column.prop(props, "use_decimate")

        col_decimate = column.column()
        col_decimate.enabled = props.use_decimate
        col_decimate.prop(props, "decimate_ratio")

        column.prop(props, "separate_by_loose_parts")
        column.prop(props, "center_to_origin")

        column.separator()
        column.label(text="Export")
        column.prop(props, "is_preview")
        column.prop(props, "increment_from")
        column.prop(props, "export_path")

        layout.operator(TextMeshCreatorOperation.bl_idname, text="Generate")
