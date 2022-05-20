# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup


class TextMeshCreatorProperties(PropertyGroup):
    def separator_items(self, context):
        return [
            ("SPACE", "Space", "Separate Strings by Space"),
            ("TAB", "Tab", "Separate Strings by Tab"),
            ("CHARACTER", "Character", "Separate Strings by Character"),
            ("NONE", "None", "Do not separate"),
        ]

    def align_x(self, context):
        return [
            ("LEFT", "Left", "Align text to the left"),
            ("CENTER", "Center", "Center text"),
            ("RIGHT", "Right", "Align text to the right"),
            ("JUSTIFY", "Justify", " Align to the left and the right"),
            ("FLUSH", "Flush", "Align to the left and the right, with equal character spacing")
        ]

    def align_y(self, context):
        return [
            ("TOP_BASELINE", "Top Baseline", "Align to top but use the base-line of the text"),
            ("TOP", "Top", "Align text to the top"),
            ("CENTER", "Center", "Align text to the middle"),
            ("BOTTOM", "Bottom", "Align text to the bottom"),
            ("BOTTOM_BASELINE", "Bottom Baseline", "Align text to the bottom but use the base-line of the text"),
        ]

    # generic
    strings: StringProperty(default="", name="Strings", description="Strings to be generated", options={"HIDDEN"})
    rotation_x: FloatProperty(default=90.0, name="Rotation X", description="Rotation X for Text", options={"HIDDEN"})
    rotation_y: FloatProperty(default=0.0, name="Rotation Y", description="Rotation Y for Text", options={"HIDDEN"})
    rotation_z: FloatProperty(default=180.0, name="Rotation Z", description="Rotation Z for Text", options={"HIDDEN"})
    scale_x: FloatProperty(default=1.0, name="Scale X", description="Scales X for Text", options={"HIDDEN"})
    scale_y: FloatProperty(default=1.0, name="Scale Y", description="Scales Y for Text", options={"HIDDEN"})
    scale_z: FloatProperty(default=1.0, name="Scale Z", description="Scales Z for Text", options={"HIDDEN"})

    font_path: StringProperty(default="", name="Font", description="Font used for mesh generation",
                              subtype="FILE_PATH", options={"HIDDEN"})
    separate_by: EnumProperty(default=3, items=separator_items, name="Separate By",
                              description="How to separate strings", options={"HIDDEN"})

    # text layout
    size: FloatProperty(default=1.0, name="Size", description="Font Size of mesh to be generated", options={"HIDDEN"})
    thickness: FloatProperty(default=0.1, name="Thickness",
                             description="Thickness of mesh to be generated", options={"HIDDEN"})
    horizontal_alignment: EnumProperty(default=0, items=align_x, name="Horizontal Alignment",
                                       description="Horizontal Alignment for Paragraph", options={"HIDDEN"})
    vertical_alignment: EnumProperty(default=0, items=align_y, name="Vertical Alignment",
                                     description="Vertical Alignment for Paragraph", options={"HIDDEN"})
    character_spacing: FloatProperty(default=1.2, name="Character Spacing",
                                     description="Spaces between characters (ignored for separated by character)", options={"HIDDEN"})
    word_spacing: FloatProperty(default=0.2, name="Word Spacing",
                                description="Space between words (ignored for separated by character or tab)", options={"HIDDEN"})

    # blendshape
    use_blendshape: BoolProperty(default=False, name="Use Blendshape",
                                 description="Move characters with Blendshapes", options={"HIDDEN"})
    blendshape_min_x: FloatProperty(default=0.0, name="Blendshape Move Min X",
                                    description="Blendshape offsets for moving to X", options={"HIDDEN"})
    blendshape_max_x: FloatProperty(default=0.0, name="Blendshape Move Max X",
                                    description="Blendshape offsets for moving to X", options={"HIDDEN"})
    blendshape_min_y: FloatProperty(default=0.0, name="Blendshape Move Min Y",
                                    description="Blendshape offsets for moving to Y", options={"HIDDEN"})
    blendshape_max_y: FloatProperty(default=0.0, name="Blendshape Move Max Y",
                                    description="Blendshape offsets for moving to Y", options={"HIDDEN"})
    blendshape_min_z: FloatProperty(default=0.0, name="Blendshape Move Min Z",
                                    description="Blendshape offsets for moving to Z", options={"HIDDEN"})
    blendshape_max_z: FloatProperty(default=0.0, name="Blendshape Move Max Z",
                                    description="Blendshape offsets for moving to Z", options={"HIDDEN"})

    # mesh
    use_decimate: BoolProperty(default=False, name="Use Decimate",
                               description="Set to True if using mesh decimate", options={"HIDDEN"})
    decimate_ratio: FloatProperty(default=0.5, name="Decimate Ratio", description="Decimate Ratio", options={"HIDDEN"})
    separate_by_loose_parts: BoolProperty(default=True, name="Separate by Loose Parts",
                                          description="Separate character by loose parts", options={"HIDDEN"})
    center_to_origin: BoolProperty(default=False, name="Center to Origin",
                                   description="Set to True if want to center of the text to be the origin", options={"HIDDEN"})

    # export
    is_preview: BoolProperty(default=False, name="Enable Preview Mode",
                             description="Set to True if want to check the generation result according to the set value", options={"HIDDEN"})
    inline_fbx: BoolProperty(default=False, name="Export as inline FBX",
                             description="Set to True if export multiple separated character(s) as single FBX", options={"HIDDEN"})
    increment_from: IntProperty(default=0, name="Increment From",
                                description="Offset value of serial number for output file", options={"HIDDEN"})
    export_path: StringProperty(default="", name="Export Directory",
                                description="Export FBX to", subtype="DIR_PATH", options={"HIDDEN"})
