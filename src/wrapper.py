# -------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# -------------------------------------------------------------------------------------------

from typing import Any, List, overload

from bpy import ops
from bpy.types import Context, Object


class OperationWrapper:

    @staticmethod
    def export_fbx(context: Context, filepath: str, objects: List[Object]) -> None:
        override = context.copy()
        override["selected_objects"] = objects

        ops.export_scene.fbx(
            override,
            filepath=filepath,
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

    @staticmethod
    def delete_object(context: Context, objects: List[Object]) -> None:
        override = context.copy()
        override["selected_objects"] = objects
        ops.object.delete(override, confirm=False)

    @staticmethod
    def separate_object(context: Context, objects: List[Object], type: str) -> None:
        override = context.copy()
        override["selected_editable_objects"] = objects
        ops.mesh.separate(override, type=type)

    @staticmethod
    def extrude_region_move(context: Context, objects: List[Object], transform: Any = None) -> None:
        override = context.copy()
        override["selected_editable_objects"] = objects
        ops.mesh.extrude_region_move(override, TRANSFORM_OT_translate=transform)

    @staticmethod
    def set_origin(context: Context, objects: List[Object], type: str, center: str) -> None:
        override = context.copy()
        override["selected_editable_objects"] = objects
        ops.object.origin_set(override, type=type, center=center)

    @staticmethod
    def select_all_in_mesh(context: Context, objects: List[Object]) -> None:
        override = context.copy()
        override["selected_editable_objects"] = objects
        ops.mesh.select_all(override, action="SELECT")

    @staticmethod
    def make_normals_consistent(context: Context, objects: List[Object], inside: bool) -> None:
        override = context.copy()
        override["selected_editable_objects"] = objects
        ops.mesh.normals_make_consistent(override, inside=inside)

    @staticmethod
    def add_modifier(context: Context, object: Object, type: str) -> None:
        override = context.copy()
        override["object"] = object
        ops.object.modifier_add(override, type=type)

    @staticmethod
    def apply_modifier(context: Context, object: Object, modifier: str) -> None:
        override = context.copy()
        override["object"] = object
        ops.object.modifier_apply(override, modifier=modifier)
