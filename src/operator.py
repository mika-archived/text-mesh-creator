# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

from __future__ import annotations

import bpy
import math
import numpy as np

from bpy.types import Object, Operator, VectorFont
from os import path

from .properties import TextMeshCreatorProperties
from .utils import replace_invalid_filename_chars
from .wrapper import OperationWrapper


class TextMeshCreatorOperation(Operator):
    bl_idname = "object.text_mesh_creator_operation"
    bl_label = "TextMeshCreator Operation"

    def separators(self):
        return {
            "SPACE": " ",
            "TAB": "\t"
        }

    def export_object(self, number: int, name: str, dirpath: str, objects: list[Object]) -> int:
        try:
            filename = replace_invalid_filename_chars("%s-%s.fbx" % (number, name))
            filepath = path.join(dirpath, filename)

            OperationWrapper.export_fbx(context=bpy.context, filepath=filepath, objects=objects)
            return number + 1
        except RuntimeError as e:
            print(e)
            return number
        finally:
            OperationWrapper.delete_object(context=bpy.context, objects=objects)

    def separate_by_loose_parts(self, object: Object, rotation: list[float], extrude: float) -> list[Object]:
        OperationWrapper.separate_object(context=bpy.context, objects=[object], type="LOOSE")

        separated_objects = bpy.context.selected_objects
        objects = []

        rotation_x = (rotation[0] - math.radians(90)) * -1
        rotation_y = (rotation[1] - math.radians(0)) * 1
        rotation_z = (rotation[2] - math.radians(180)) * 1

        # rotate the base object to align the object's decision axis
        rot_x = np.array([
            [1, 0, 0],
            [0, math.cos(rotation_x), -math.sin(rotation_x)],
            [0, math.sin(rotation_x), math.cos(rotation_x)]
        ])
        rot_y = np.array([
            [math.cos(rotation_y), 0, -math.sin(rotation_y)],
            [0, 1, 0],
            [math.sin(rotation_y), 0, math.cos(rotation_y)]
        ])
        rot_z = np.array([
            [math.cos(rotation_z), -math.sin(rotation_z), 0],
            [math.sin(rotation_z), math.cos(rotation_z), 0],
            [0, 0, 1]
        ])

        # dir vector
        dec_vector_h = np.array([1, 0, 0])
        dec_vector_h = rot_x @ dec_vector_h
        dec_vector_h = rot_y @ dec_vector_h
        dec_vector_h = rot_z @ dec_vector_h
        dec_vector_h = dec_vector_h / np.linalg.norm(dec_vector_h)

        # dir vector
        dec_vector_v = np.array([0, 0, 1])
        dec_vector_v = rot_x @ dec_vector_v
        dec_vector_v = rot_y @ dec_vector_v
        dec_vector_v = rot_z @ dec_vector_v
        dec_vector_v = dec_vector_v / np.linalg.norm(dec_vector_v)

        # dir vector
        dec_vector_b = np.array([0, 0, 0])

        # pos vector
        dec_vector_p = np.array([0, extrude, 0])
        dec_vector_p = rot_x @ dec_vector_p
        dec_vector_p = rot_y @ dec_vector_p
        dec_vector_p = rot_z @ dec_vector_p

        for object in separated_objects:
            vertices = []
            for vertex in object.data.vertices:
                origin = np.array([vertex.co.x, vertex.co.y, vertex.co.z])

                # see: https://manabitimes.jp/math/1197
                ab = (dec_vector_p + dec_vector_h - origin)
                ac = (dec_vector_p + dec_vector_v - origin)
                ad = (dec_vector_p + dec_vector_b - origin)

                matrix = np.array([
                    [ab[0], ac[0], ad[0]],
                    [ab[1], ac[1], ad[1]],
                    [ab[2], ac[2], ad[2]]
                ])

                r = np.linalg.det(matrix)

                vertices.append(math.isclose(r, 0, abs_tol=1e-5))

            if not all(vertices):
                OperationWrapper.delete_object(context=bpy.context, objects=[object])
                continue

            objects.append(object)

        # bulk edit
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="FACE")

        dec_vector_e = np.array([0, extrude * -2, 0])
        dec_vector_e = rot_x @ dec_vector_e
        dec_vector_e = rot_y @ dec_vector_e
        dec_vector_e = rot_z @ dec_vector_e

        OperationWrapper.select_all_in_mesh(context=bpy.context, objects=objects)
        OperationWrapper.extrude_region_move(context=bpy.context, objects=objects,
                                             transform={"value": dec_vector_e})
        OperationWrapper.select_all_in_mesh(context=bpy.context, objects=objects)
        OperationWrapper.make_normals_consistent(context=bpy.context, objects=objects, inside=False)

        bpy.ops.object.mode_set(mode="OBJECT")

        return objects

    def create_object(self, number: int, text: str, font: VectorFont, props: TextMeshCreatorProperties) -> bool:
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

        if props.center_to_origin:
            font_object_f.location = (0, 0, 0)

        if props.use_decimate:
            OperationWrapper.add_modifier(context=bpy.context, object=font_object_f, type="DECIMATE")

            font_object_f.modifiers[0].ratio = props.decimate_ratio

            OperationWrapper.apply_modifier(context=bpy.context, object=font_object_f,
                                            modifier=font_object_f.modifiers[0].name)

        if props.separate_by_loose_parts:
            objects = self.separate_by_loose_parts(font_object_f, rotation, props.thickness)
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
            number = self.create_object(number, character, font, props)

        return {"FINISHED"}
