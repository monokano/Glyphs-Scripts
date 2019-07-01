[English](https://github.com/monokano/Glyphs-Scripts) / [日本語](README-JP.md)

# Scripts for Glyphs

## Description

### Switch Direction
  * Toggle the writing direction of Edit View to update the info display.

#### How to use
This script has the panel window. Push the buttons on the panel to switch.

### Make vrt2 Glyph
  * Creates a new vrt2 (.rotat) glyph based on the selected glyphs.
  * The .rotat glyph has its base glyph as a component.
    * If the .rotat glyph already exists, the base glyph is placed as a component.
  * If the selected glyph is a .rotat glyph, the base glyph is placed as a component.
    * If the base glyph does not exist, the selected .rotat glyph will be removed.
  * If the width of the base glyph is greater than or equal to Em, the .rotat glyph is not created. 
    * If The .rotat glyph already exists, it will be removed.
#### How to use
Select the glyphs in List View before running this script. Be sure to update the feature after running. No Python module required.

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).