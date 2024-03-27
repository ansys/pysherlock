# © 2024 ANSYS, Inc. All rights reserved.

"""Module containing types for the Project Service."""

try:
    import SherlockProjectService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockProjectService_pb2

project_service = SherlockProjectService_pb2


class BoardBounds:
    """Contains the properties of the board bounds."""

    def __init__(self, bounds):
        """Initialize the board bounds."""
        self.bounds = bounds
        """bounds (two tuples of the form (x, y) : list[tuple[float, float]]"""


class CsvExcelFile:
    """Contains the properties for a thermal map csv or excel file."""

    def __init__(
        self,
        header_row_count,
        numeric_format,
        reference_id_column,
        temperature_column,
        temperature_units,
    ):
        """Initialize the thermal map csv or excel file properties."""
        self.header_row_count = header_row_count
        """header_row_count: int"""
        self.numeric_format = numeric_format
        """numeric_format: string"""
        self.reference_id_column = reference_id_column
        """reference_id_column: string"""
        self.temperature_column = temperature_column
        """temperature_column: string"""
        self.temperature_units = temperature_units
        """temperature_units: string"""


class IcepakFile:
    """Contains the properties for a thermal map Icepak file."""


class ImageBounds:
    """Contains the properties of the image bounds."""

    def __init__(self, image_x, image_y, height, width):
        """Initialize the image bounds properties."""
        self.image_x = image_x
        """x coordinate of the upper left corner : float"""
        self.image_y = image_y
        """y coordinate of the upper left corner : float"""
        self.height = height
        """height of the image : float"""
        self.width = width
        """width of the image : float"""


class ImageFile:
    """Contains the properties for a thermal map image file."""

    def __init__(
        self,
        board_bounds,
        coordinate_units,
        image_bounds,
        legend_bounds,
        legend_orientation,
        max_temperature,
        max_temperature_units,
        min_temperature,
        min_temperature_units,
    ):
        """Initialize the thermal image file properties."""
        self.board_bounds = board_bounds
        """board_bounds : BoardBounds"""
        self.coordinate_units = coordinate_units
        """coordinate_units : string"""
        self.image_bounds = image_bounds
        """image_bounds : ImageBounds"""
        self.legend_bounds = legend_bounds
        """legend_bounds : LegendBounds"""
        self.legend_orientation = legend_orientation
        """legend_orientation : LegendOrientation"""
        self.max_temperature = max_temperature
        """max_temperature : float"""
        self.max_temperature_units = max_temperature_units
        """max_temperature_units : string"""
        self.min_temperature = min_temperature
        """min_temperature : float"""
        self.min_temperature_units = min_temperature_units
        """min_temperature_units : string"""


class LegendBounds:
    """Contains the properties of the legend bounds."""

    def __init__(self, legend_x, legend_y, height, width):
        """Initialize the legend bounds properties."""
        self.legend_x = legend_x
        """x coordinate of the upper left corner : float"""
        self.legend_y = legend_y
        """y coordinate of the upper left corner : float"""
        self.height = height
        """height of the legend : float"""
        self.width = width
        """width of the legend : float"""


class LegendOrientation:
    """Constants for legend orientation in the update thermal maps request."""

    __legend_orientation = project_service.ThermalMapFile.ImageFile.LegendOrientation
    HORIZONTAL = __legend_orientation.Horizontal
    "Horizontal"
    VERTICAL = __legend_orientation.Vertical
    "Vertical"


class ThermalBoardSide:
    """Constants for thermal board side in the update thermal maps request."""

    __thermal_board_side = project_service.ThermalMapFile.ThermalBoardSide
    BOTTOM = __thermal_board_side.Bottom
    "Bottom"
    BOTH = __thermal_board_side.Both
    "Both"
    TOP = __thermal_board_side.Top
    "Top"


class ThermalMapsFileType:
    """Constants for File Type in the Update Thermal Maps request."""

    __file_type = project_service.ThermalMapFile.FileType
    CSV = __file_type.CSV
    "CSV"
    EXCEL = __file_type.Excel
    "Excel"
    IMAGE = __file_type.Image
    "Image"
    TMAP = __file_type.TMAP
    "Icepak Thermal Map (.TMAP)"


class StrainMapsFileType:
    """Constants for File Type in the Add Strain Maps request."""

    __file_type = project_service.AddStrainMapRequest.StrainMapFile.FileType
    CSV = __file_type.CSV
    "CSV"
    EXCEL = __file_type.Excel
    "Excel"
    IMAGE = __file_type.Image
    "Image"


class StrainMapLegendOrientation:
    """Constants for legend orientation in the add strain maps request."""

    __legend_orientation = (
        project_service.AddStrainMapRequest.StrainMapFile.StrainMapImageFile.LegendOrientation
    )
    HORIZONTAL = __legend_orientation.Horizontal
    "Horizontal"
    VERTICAL = __legend_orientation.Vertical
    "Vertical"
