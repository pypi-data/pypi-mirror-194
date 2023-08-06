import klayout.db as db
import klayout.lib
import numpy as np
import os
import importlib.resources
from . import alignment

lib_basic = db.Library.library_by_name("Basic")
ly = db.Layout()
# sets unit to micrometer
LY_DBU = ly.dbu


def export_layer_gds(filename):
    for layer_index, layer_info in zip(ly.layer_indexes(), ly.layer_infos()):
        parameters_saving = db.SaveLayoutOptions()
        parameters_saving.add_layer(layer_index, layer_info)
        ly.write(filename+'_layer'+str(layer_index)+'.gds', parameters_saving)


def export_design_gds(filename):
    ly.write(filename+'.gds')


# sets path of alignment mark files
with importlib.resources.path(alignment, "alignment_square.GDS") as p:
    ALIGN_SQUARE_PATH = str(p)


class AbstractPolygon:
    """
    AbstractPolygon is the parent class of different types of polygons (rectangle, circles).
    It is an abstract class and never directly instantiated.
    
    Parameters
    ----------
    name : str
        Name of the AbstractPolygon
    polygon_db : KLayout polygon
        The created polygon object
    centered : bool, optional
        Specifies if the object is drawn from its geometrical center (True) or from the bottom left corner (False)
    dx : int, optional
        Movement in x direction in um
    dy : int, optional
        Movement in y direction in um
    rotation : int, optional
        Rotation in degrees
    magnification : int, optional
        Magnifying factor
    mirrorx : bool, optional
        Mirror in x direction
    """
    def __init__(self, name: str, polygon_db, centered=True, dx=0, dy=0, rotation=0, magnification=1, mirrorx=False):
        self.name = name
        self.centered = centered
        self.polygon_db = polygon_db
        self.transformation(dx, dy, rotation, magnification, mirrorx)

    def transformation(self, dx, dy, rotation=0, magnification=1, mirrorx=False):
        """
        Transformation allows to move, rotate, magnify and mirror a polygon or text
        
        Parameters
        ----------
        dx : float
            Movement in x direction in um
        dy : float
            Movement in y direction in um
        rotation : int, optional
            Rotation in degrees
        magnification : int, optional
            Magnifying factor
        mirrorx : bool, optional
            Mirror in x direction
        """
        complex_transformation = db.ICplxTrans(magnification, rotation, mirrorx, int(dx/LY_DBU), int(dy/LY_DBU))
        if hasattr(self, 'polygon_db'):
            self.polygon_db.transform(complex_transformation)
        else:
            self.region_db.transform(complex_transformation)


class Rectangle(AbstractPolygon):
    """
    Rectangle class inherits from AbstractPolygon class and allows to create a rectangular polygon.
    
    Parameters
    ----------
    name : str
        Name of the rectangular polygon object
    x : float
        Width of the rectangle
    y : float
        Height of the rectangle
    centered : bool, optional
        Specifies if the object is drawn from its geometrical center (True) or from the bottom left corner (False)
    dx : int, optional
        Movement in x direction in um
    dy : int, optional
        Movement in y direction in um
    rotation : int, optional
        Rotation in degrees
    magnification : int, optional
        Magnifying factor
    mirrorx : bool, optional
        Mirror in x direction
    """
    def __init__(self, name: str, x: float, y: float, centered=True, dx=0, dy=0, magnification=1, rotation=0,
                 mirrorx=False):
        self.x = x
        self.y = y
        self.centered = centered

        x_um = self.x/LY_DBU
        y_um = self.y/LY_DBU
        if self.centered:
            point_rectangle = [db.DPoint(-x_um/2, -y_um/2), db.DPoint(x_um/2, -y_um/2),
                               db.DPoint(x_um/2, y_um/2), db.DPoint(-x_um/2, y_um/2)]
        else:
            point_rectangle = [db.DPoint(0, 0), db.DPoint(x_um, 0), db.DPoint(x_um, y_um), db.DPoint(0, y_um)]

        self.polygon_db = db.Polygon(point_rectangle)
        super().__init__(name, self.polygon_db, centered, dx, dy, rotation, magnification, mirrorx)


class Circle(AbstractPolygon):
    """
    Circle class allows to create a circular polygon object and inherits from AbstractPolygon class.
    
    Parameters
    ----------
    name : str
        Name of the circular polygon object
    radius : float
        Radius of circle
    centered : bool, optional
        Specifies if the object is drawn from its geometrical center (True), always True for circle
    nr_points : int, optional
        Number of points used to draw the circular polygon
    dx : int, optional
        Movement in x direction in um
    dy : int, optional
        Movement in y direction in um
    rotation : int, optional
        Rotation in degrees
    magnification : int, optional
        Magnifying factor
    mirrorx : bool, optional
        Mirror in x direction
    """
    def __init__(self, name: str, radius: float, centered=True, nr_points=64, dx=0, dy=0, rotation=0, magnification=1,
                 mirrorx=False):
        self.radius = radius
        self.nr_points = nr_points

        radius = self.radius/LY_DBU
        angles = np.linspace(0, 2*np.pi, self.nr_points + 1)[0:-1]
        points = []  # array of points
        for angle in angles:
            points.append(db.Point(radius*np.cos(angle), radius*np.sin(angle)))
        self.polygon_db = db.Polygon(points)
        super().__init__(name, self.polygon_db, centered, dx, dy, rotation, magnification, mirrorx)


class Region:
    """
    Region class allows to create regions from a list of polygons (such as rectangle or circle).
    Regions can be used for boolean operations.
    
    Parameters
    ----------
    polygon_object_list : list
        List of Polygon
    """
    def __init__(self, polygon_object_list: list):
        self.polygon_db_list = [polygon_object.polygon_db for polygon_object in polygon_object_list]
        self.region_db = db.Region(self.polygon_db_list)

    def subtract(self, region_to_subtract):
        """
        Subtract a region from another one. The boolean result is stored in the original region.
            
        Parameters
        ----------
        region_to_subtract : TYPE
            Region to subtract from the original region
        """
        self.region_db = self.region_db - region_to_subtract.region_db

    def add(self, region_to_add):
        """
        Add a region from another one. The boolean result is stored in the original region.
        
        Parameters
        ----------
        region_to_add : TYPE
            Region to add from the original region
        """
        self.region_db = self.region_db + region_to_add.region_db


class Cell:
    """
    A cell is one of the building blocks of the layout. It can contain any type of object (polygon, region, text, etc...).
    
    Parameters
    ----------
    name : str
        Name of the cell
    gds_path : str, optional
        GDS path when importing external .gds file, such as alignment mark.
    """
    def __init__(self, name: str, gds_path=''):
        if gds_path:
            # https://www.klayout.org/klayout-pypi/examples/layout_merge/
            ly_import = db.Layout()
            ly_import.read(gds_path)
            imported_top_cell = ly_import.top_cell()

            self.name = name
            gds_cell = ly.create_cell(self.name)
            gds_cell.copy_tree(imported_top_cell)

            # frees the resources of the imported layout
            ly_import._destroy()

            self.layers = {}  # dict with layers as keys
            self.cell = gds_cell
        else:
            self.name = name
            self.layers = {}  # dict with layers as keys
            self.cell = ly.create_cell(self.name)

    def draw_polygon(self, polygon_object, target_layer):
        """
        Draw a polygon on the cell in the specified layer.

        Parameters
        ----------
        polygon_object : TYPE
            Polygon object (rectangle, circle) to draw
        target_layer : TYPE
            Layer to draw the object in
        """
        self.cell.shapes(target_layer).insert(polygon_object.polygon_db)
        # it would be nice if we could add multiple polygons at the same time/to multiple layers at the same time

    def draw_path(self, path_object, target_layer):
        """
        Draw a path on the cell in the specified layer.
        
        Parameters
        ----------
        path_object : TYPE
            Path object to draw
        target_layer : TYPE
            Layer to draw the object in
        """
        self.cell.shapes(target_layer).insert(path_object.path)

    def draw_region(self, region, target_layer):
        """
        Draw a region on the cell in the specified layer.
        
        Parameters
        ----------
        region : TYPE
            Region to draw
        target_layer : TYPE
            Layer to draw the object in
        """
        self.cell.shapes(target_layer).insert(region.region_db)

    def draw_text(self, text_region, target_layer):
        """
        Draw a text on the cell in the specified layer.
        
        Parameters
        ----------
        text_region : TYPE
            Text to draw
        target_layer : TYPE
            Layer to draw the object in
        """
        self.cell.shapes(target_layer).insert(text_region.region_db)

    def insert_cell(self, cell_to_insert, origin_x=0, origin_y=0, rotation=0, magnitude=1, mirrorx=False):
        """
        Insert a cell in the current cell. The inserted cell can be placed, rotated, magnified and mirrored.
        
        Parameters
        ----------
        cell_to_insert : TYPE
            Cell to insert in the current cell
        origin_x : int, optional
            x coordinate in the current cell of the center of the inserted cell in um
        origin_y : int, optional
            y coordinate in the current cell of the center of the inserted cell in um
        rotation : int, optional
            Rotation in degree
        magnitude : int, optional
            Magnification of the cell
        mirrorx : bool, optional
            Mirror in x direction
        """
        complex_transformation = db.ICplxTrans(magnitude, rotation, mirrorx, int(origin_x/LY_DBU),
                                               int(origin_y/LY_DBU))
        cell_instance = db.CellInstArray(cell_to_insert.cell.cell_index(), complex_transformation)
        self.cell.insert(cell_instance)

    def insert_cell_array(self, cell_to_insert, x_row, y_row, x_column, y_column, n_row: int, n_column: int,
                          origin_x=0, origin_y=0, rotation=0, magnitude=1, mirrorx=False):
        """
        Insert an array of cell in the current cell. The inserted cell can be placed, rotated, magnified and mirrored.
        
        Parameters
        ----------
        cell_to_insert : TYPE
            Cell to insert in the current cell
        x_row : TYPE
            x coordinate of row vector in um
        y_row : TYPE
            y coordinate of row vector in um
        x_column : TYPE
            x coordinate of column vector in um
        y_column : TYPE
            y coordinate of column vector in um
        n_row : int
            Number of row
        n_column : int
            Number of column
        origin_x : int, optional
            x coordinate in the current cell of the center of the inserted cell in um
        origin_y : int, optional
            y coordinate in the current cell of the center of the inserted cell in um
        rotation : int, optional
            Rotation in degree
        magnitude : int, optional
            Magnification of the cell
        mirrorx : bool, optional
            Mirror in x direction
        """
        v_row = db.Vector(x_row/LY_DBU, y_row/LY_DBU)
        v_column = db.Vector(x_column/LY_DBU, y_column/LY_DBU)
        complex_transformation = db.ICplxTrans(magnitude, rotation, mirrorx, int(origin_x/LY_DBU),
                                               int(origin_y/LY_DBU))
        cell_instance_array = db.CellInstArray(cell_to_insert.cell.cell_index(), complex_transformation, v_row,
                                               v_column, n_row, n_column)
        self.cell.insert(cell_instance_array)

    def flatten(self):
        """
        Flatten the layout squishing every children cell on the current cell.
        """
        self.cell.flatten(-1, True)

    def export_design_gds(self, filename):
        parameters_saving = db.SaveLayoutOptions()
        parameters_saving.add_cell(self.cell.cell_index())
        ly.write(filename + '.gds', parameters_saving)

    def export_layer_gds(self, filename):
        for layer_index, layer_info in zip(ly.layer_indexes(), ly.layer_infos()):
            parameters_saving = db.SaveLayoutOptions()
            parameters_saving.add_cell(self.cell.cell_index())
            parameters_saving.add_layer(layer_index, layer_info)
            ly.write(filename + '_layer' + str(layer_index) + '.gds', parameters_saving)


class Path:
    """
    Path is a class used to create paths connecting different objects.
    
    Parameters
    ----------
    points : list
        List of points that the path should follow and connect
    width : float
        Width of the path
    """
    def __init__(self, points: list, width: float):
        self.points = points
        self.width = width
        self.path = db.Path([point/LY_DBU for point in self.points], self.width/LY_DBU)


class Text(AbstractPolygon):
    """
    Text class inherits from AbstractPolygon class and allows to generate text for labelling layouts.

    Parameters
    ----------
    text : str
        Text that needs to be generated
    magnification : int, optional
        Magnifying factor
    dx : int, optional
        Movement in x direction in um
    dy : int, optional
        Movement in y direction in um
    rotation : int, optional
        Rotation in degrees
    mirrorx : bool, optional
        Mirror in x direction
    """
    def __init__(self, text: str, magnification=1000, dx=0, dy=0, rotation=0, mirrorx=False):
        self.generator = db.TextGenerator().default_generator()
        self.region_db = self.generator.text(text, LY_DBU, magnification)

        dx_region = self.region_db.bbox().width() * LY_DBU
        dy_region = self.region_db.bbox().height() * LY_DBU
        self.transformation(-dx_region/2+dx, -dy_region/2+dy, rotation, 1, mirrorx)
