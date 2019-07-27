[English](https://github.com/monokano/Glyphs-Scripts) / [日本語](README-JP.md)

# Scripts for Glyphs

## Description

### Make Rect Path
  * Adds a rectangular path to the glyph.
  * Settings:
      * Target Glyph: Selection/All
      * Rectangle type: White (Line box)/Black (Fill)
         * You can set the line width.
      * Rectangular Size: Body/Bounds (Path Area).
         * You can set the offset value.
      * Lets you set whether to empty the glyph before adding a rectangular path.

#### How to use
This script has the panel window. Configure the settings on the window and press the Run button. Requires Python module.


### Switch Direction
  * Toggle the writing direction of Edit View to update the info display.

#### How to use
This script has the panel window. Push the buttons on the panel to switch. Requires Python module.

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

### Set vrt2 VertWidth
  * Set the vertWidth of the vrt2 glyph (.rotat) to be the same as the Width of the component.
  * The .rotat glyph must have one component.
      * Do nothing if there are no component or if there are multiple components.
#### How to use
Execute in the Script menu. All .rotat glyphs are affected. No Python module required.

## License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).