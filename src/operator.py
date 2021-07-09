# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

import bpy
from bpy.types import Object, Operator, TextCurve, VectorFont
import math
from os import path

from .properties import TextMeshCreatorProperties


class TextMeshCreatorOperation(Operator):
    bl_idname = "object.text_mesh_creator_operation"
    bl_label = "TextMeshCreator Operation"

    def separators(self):
        return {
            "SPACE": " ",
            "TAB": "\t"
        }

    def create_object(self, number: int, text: str, font: VectorFont, props: TextMeshCreatorProperties) -> bool:
        font_curve: TextCurve = bpy.data.curves.new(type="FONT", name="Font Curve")
        font_curve.body = text
        font_curve.font = font
        font_curve.extrude = props.thickness
        font_curve.align_x = props.horizontal_alignment
        font_curve.align_y = props.vertical_alignment
        font_curve.space_character = props.character_spacing
        font_curve.space_word = props.word_spacing

        font_object: Object = bpy.data.objects.new(name=text, object_data=font_curve)
        font_object.location = (0, 0, 0)
        font_object.rotation_euler.x = math.radians(props.rotation_x)
        font_object.rotation_euler.y = math.radians(props.rotation_y)
        font_object.rotation_euler.z = math.radians(props.rotation_z)
        font_object.scale.x = props.scale_x
        font_object.scale.y = props.scale_y
        font_object.scale.z = props.scale_z

        bpy.context.scene.collection.objects.link(font_object)

        override = bpy.context.copy()
        override["selected_editable_objects"] = [font_object]
        bpy.ops.object.origin_set(override, type="ORIGIN_GEOMETRY", center="BOUNDS")

        if props.center_to_origin:
            font_object.location = (0, 0, 0)

        try:
            override = bpy.context.copy()
            override["selected_objects"] = [font_object]
            filename = "%s-%s.fbx" % (number, text)

            print(path.join(props.export_path, filename))

            bpy.ops.export_scene.fbx(override,
                                     filepath=path.join(props.export_path, filename),
                                     check_existing=True,
                                     filter_glob="*.fbx",
                                     use_selection=True,
                                     use_active_collection=False,
                                     global_scale=1.0,
                                     apply_unit_scale=True,
                                     apply_scale_options="FBX_SCALE_NONE",
                                     bake_space_transform=False,
                                     object_types={"ARMATURE", "MESH", "OTHER"},
                                     use_mesh_modifiers=False,
                                     use_mesh_modifiers_render=False,
                                     mesh_smooth_type="OFF",
                                     use_subsurf=False,
                                     use_mesh_edges=False,
                                     use_tspace=False,
                                     use_custom_props=False,
                                     add_leaf_bones=False,
                                     primary_bone_axis="Y",
                                     secondary_bone_axis="X",
                                     use_armature_deform_only=False,
                                     armature_nodetype="NULL",
                                     bake_anim=False,
                                     path_mode="AUTO",
                                     embed_textures=False,
                                     batch_mode="OFF",
                                     use_metadata=True,
                                     axis_forward="-Z",
                                     axis_up="Y"
                                     )
            return number + 1
        except RuntimeError as e:
            print(e)
            return number
        finally:
            # cleanup
            override = bpy.context.copy()
            override["selected_objects"] = [font_object]
            bpy.ops.object.delete(override)

    def execute(self, context):
        props: TextMeshCreatorProperties = context.scene.TextMeshCreatorProperties
        font: VectorFont
        number: int = props.increment_from

        if props.font_path.strip() != "":
            try:
                font = bpy.data.fonts.load(props.font_path)
            except RuntimeError:
                self.report({"ERROR"}, "Font file not found or invalid format.")
                return {"CANCELLED"}

        if props.separate_by == "CHARACTER":
            characters = list(props.strings)
            for character in characters:
                number = self.create_object(number, character, font, props)
        elif props.separate_by != "NONE":
            characters = props.strings.split(self.separators()[props.separate_by])
            for character in characters:
                number = self.create_object(number, character, font, props)
        else:
            number = self.create_object(number, props.strings, font, props)

        return {"FINISHED"}
