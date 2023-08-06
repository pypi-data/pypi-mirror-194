from koala.classes import *

# File information for the .gds file
filename = 'example1'

# Creation of all the necessary layers for the layout
gold_layer = ly.layer(0, 0)
osc_layer = ly.layer(1, 0)

# Creation of the bottom cell which will have a square with a hollow center
bottom_cell = Cell(name='BOTTOM')
# 2 polygons are created to help us create the hollow electrode
square_hole = Circle(name='electrode_hole', radius=100)
square = Rectangle(name='electrode', x=200, y=200)
# The 2 polygons are transformed into regions so boolean operation can be made
center = Region(polygon_object_list=[square_hole])
border = Region(polygon_object_list=[square])
# To do boolean operation on Region, methods can be applied directly to Region class such as subtract or add
border.subtract(region_to_subtract=center)
# The final Region (border with a hole inside) has been made, but we still need to draw it in a certain cell on a
# certain layer. To do that, a method is available within the Cell class
bottom_cell.draw_region(region=border, target_layer=gold_layer)

# A second cell is created. We will insert an array of the hollow square we just created, and we will add some text
top_cell = Cell(name='TOP')
# We insert an array of a cell by using another method from the Cell object
top_cell.insert_cell_array(cell_to_insert=bottom_cell, x_row=0, y_row=100, x_column=100, y_column=0, n_row=2, n_column=3)

# We create a Text object and apply a transformation to move it and rotate it
text = Text(text='Example', magnification=20, dx=-125, dy=0, rotation=90)
# We now draw the text that has been created and transformed
top_cell.draw_text(text_region=text, target_layer=osc_layer)

# Flattening allows to delete the different Cells and have a clean top Cell
top_cell.flatten()

# Finally, we export the design of the top_cell in a .gds file
top_cell.export_design_gds(filename)
# Finally, we export each layer of the top_cell in a different .gds file
top_cell.export_layer_gds(filename)
