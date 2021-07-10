# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

from typing import List
import bpy
from bpy.types import Context, Object, Operator, VectorFont
import math
from mathutils import Vector
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

    def export_object(self, number: int, name: str, dirpath: str, object: List[Object]) -> int:
        try:
            override = bpy.context.copy()
            override["selected_objects"] = object
            filename = "%s-%s.fbx" % (number, name)

            bpy.ops.export_scene.fbx(override,
                                     filepath=path.join(dirpath, filename),
                                     check_existing=True,
                                     filter_glob="*.fbx",
                                     use_selection=True,
                                     use_active_collection=False,
                                     global_scale=1.0,
                                     apply_unit_scale=True,
                                     apply_scale_options="FBX_SCALE_ALL",
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
            override["selected_objects"] = object
            bpy.ops.object.delete(override)

    def separate_by_loose_parts(self, object: Object, extrude: float) -> List[Object]:
        override = bpy.context.copy()
        override["selected_editable_objects"] = [object]
        bpy.ops.mesh.separate(override, type="LOOSE")  # override context.selected_objects

        separated_objects = bpy.context.selected_objects
        objects = []

        for object in separated_objects:
            center = 0.125 * sum((Vector(bound) for bound in object.bound_box), Vector())
            origin = object.matrix_world @ center

            if not math.isclose(origin.y, extrude, rel_tol=1e-5):
                override = bpy.context.copy()
                override["selected_objects"] = [object]
                bpy.ops.object.delete(override, confirm=False)
                continue

            override = bpy.context.copy()
            override["object"] = object
            bpy.ops.object.modifier_add(override, type="SOLIDIFY")

            object.modifiers[0].thickness = extrude * 2

            bpy.ops.object.modifier_apply(override, modifier=object.modifiers[0].name)
            objects.append(object)

        return objects

    def create_object(self, context: Context, number: int, text: str, font: VectorFont, props: TextMeshCreatorProperties) -> bool:
        rotation = (math.radians(props.rotation_x), math.radians(props.rotation_y), math.radians(props.rotation_z))

        # I can't find a way to get the ObjectBase in here :(
        # But, bpy.ops.object.text_add set the ObjectBase correctly :)
        bpy.ops.object.text_add(rotation=rotation)
        font_object_o: Object = bpy.context.object
        font_object_o.name = "OBJECT"
        font_object_o.data.name = "CURVE"
        font_object_o.data.body = text
        font_object_o.data.font = font
        font_object_o.data.extrude = props.thickness
        font_object_o.data.align_x = props.horizontal_alignment
        font_object_o.data.align_y = props.vertical_alignment
        font_object_o.data.space_character = props.character_spacing
        font_object_o.data.space_word = props.word_spacing

        bpy.context.view_layer.objects.active = font_object_o
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.transform_apply(rotation=True, scale=True, location=True)

        font_object_f: Object = bpy.context.object
        font_object_f.name = text
        font_object_f.location = (0, 0, 0)
        font_object_f.scale.x = props.scale_x
        font_object_f.scale.y = props.scale_y
        font_object_f.scale.z = props.scale_z

        override = bpy.context.copy()
        override["selected_editable_objects"] = [font_object_f]
        bpy.ops.object.origin_set(override, type="ORIGIN_GEOMETRY", center="BOUNDS")

        if props.center_to_origin:
            font_object_f.location = (0, 0, 0)

        if props.use_decimate:
            override = bpy.context.copy()
            override["object"] = font_object_f
            bpy.ops.object.modifier_add(override, type="DECIMATE")

            font_object_f.modifiers[0].ratio = props.decimate_ratio

            bpy.ops.object.modifier_apply(override, modifier=font_object_f.modifiers[0].name)

        if props.separate_by_loose_parts:
            objects = self.separate_by_loose_parts(font_object_f, props.thickness)
            if props.is_preview:
                return number
            return self.export_object(number, text, props.export_path, objects)

        if props.is_preview:
            return number
        return self.export_object(number, text, props.export_path, [font_object_f])

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

        characters = []

        if props.separate_by == "CHARACTER":
            characters = list(props.strings)
        elif props.separate_by != "NONE":
            characters = props.strings.split(self.separators()[props.separate_by])
        else:
            characters = [props.strings]

        if props.is_preview:
            characters = [characters[0]]

        for character in characters:
            number = self.create_object(context, number, character, font, props)

        return {"FINISHED"}
