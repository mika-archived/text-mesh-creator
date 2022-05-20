# Blender Add-on: TextMesh Creator

Blender add-on for creating 3D Text Objects from strings.
This is a alternative implementation of [this add-on](https://booth.pm/ja/items/1580053).
However, this implementation works with Blender LTS and is independent of the UI locale.

## Supports

- Blender 2.8x (branch #2.8)
- Blender 2.9x (branch #2.9 - old main)
- Blender 3.0x (branch #3.0 - current main)

## Installation

1. Download Installation Archive from [BOOTH](https://natsuneko.booth.pm/items/3110204).
2. Open the Preferences window and select `Add-ons` tab
3. Press `Install` button, select downloaded zip-archive and select `Install Add-on`
4. Select `Community` tab and enable `Generic: TextMeshCreator`

## How to use

1. Open `Layout` , `Modeling` or other 3D View
2. Expand sidebar and select `TextMesh Creator`
3. Configure strings, fonts, directory and other options
4. Press `Generate` button

## Available Parameters (Features)

| Parameter Name          | Type    | Default        | Description                                                                              |
| ----------------------- | ------- | -------------- | ---------------------------------------------------------------------------------------- |
| Strings                 | `str`   | `(null)`       | Strings to be generated                                                                  |
| Rotation X              | `float` | `90.0`         | Rotation X for Text (Modifies are not Recommended)                                       |
| Rotation Y              | `float` | `0.0`          | Rotation Y for Text (Modifies are not Recommended)                                       |
| Rotation Z              | `float` | `180.0`        | Rotation Z for Text (Modifies are not Recommended)                                       |
| Scale X                 | `float` | `1.0`          | Scale X for Text                                                                         |
| Scale Y                 | `float` | `1.0`          | Scale Y for Text                                                                         |
| Scale Z                 | `float` | `1.0`          | Scale Z for Text                                                                         |
| Font Path               | `str`   | `(null)`       | Font used for mesh generation                                                            |
| Separate By             | `enum`  | `NONE`         | How to separate strings (Space, Tab, Character, or None)                                 |
| Thickness               | `float` | `0.1`          | Thickness of mesh to be generated                                                        |
| Horizontal Alignment    | `enum`  | `LEFT`         | Horizontal Alignment for Paragraph (Left, Center, Right, Justify, or Flush)              |
| Vertical Alignment      | `enum`  | `TOP_BASELINE` | Vertical Alignment for Paragraph (Top Baseline, Top, Center, Bottom, or Bottom Baseline) |
| Character Spacing       | `float` | `1.2`          | Spaces between characters (ignored for separated by character)                           |
| Word Spacing            | `float` | `0.2`          | Space between words (ignored for separated by character or tab)                          |
| Use Decimate            | `bool`  | `False`        | Set to True if using mesh decimate                                                       |
| Decimate Ratio          | `float` | `0.5`          | Decimate Ratio                                                                           |
| Separate by Loose Parts | `bool`  | `True`         | Separate character by loose parts                                                        |
| Center to Origin        | `bool`  | `False`        | Set to True if want to center of the text to be the origin                               |
| Enable Preview Mode     | `bool`  | `False`        | Set to True if want to check the generation result according to the set value            |
| Increment From          | `int`   | `0`            | Offset value of serial number for output file                                            |
| Export Directory        | `str`   | `(null)`       | Export FBX to base directory path                                                        |

## Not Implemented Parameters

| Parameter Name | Type   | Default | Description                                                         |
| -------------- | ------ | ------- | ------------------------------------------------------------------- |
| Inline FBX     | `bool` | `False` | Set to True if export multiple separated character(s) as single FBX |

## License

This software is licensed under the MIT License.
