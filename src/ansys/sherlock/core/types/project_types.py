# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Project Service."""

try:
    import SherlockProjectService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockProjectService_pb2

project_service = SherlockProjectService_pb2
thermal_map_file = project_service.ThermalMapFile
add_strain_map_request = project_service.AddStrainMapRequest


class BoardBounds:
    """Contains the properties of the board bounds."""

    def __init__(self, bounds: list[tuple[float, float]]):
        """Initialize the board bounds."""
        self.bounds = bounds
        """list[tuple[float, float]]: bounds (two tuples of the form (x, y)"""


class CsvExcelFile:
    """Contains the properties for a thermal map, CSV, or Excel file."""

    def __init__(
        self,
        header_row_count: int,
        numeric_format: str,
        reference_id_column: str,
        temperature_column: str,
        temperature_units: str,
    ):
        """Initialize the thermal map, CSV or Excel file properties."""
        self.header_row_count = header_row_count
        """int: header_row_count"""
        self.numeric_format = numeric_format
        """str: numeric_format"""
        self.reference_id_column = reference_id_column
        """str: reference_id_column"""
        self.temperature_column = temperature_column
        """str: temperature_column"""
        self.temperature_units = temperature_units
        """str: temperature_units"""


class IcepakFile:
    """Contains the properties for a thermal map Icepak file."""


class ImageBounds:
    """Contains the properties of the image bounds."""

    def __init__(self, image_x: float, image_y: float, height: float, width: float):
        """Initialize the image bounds properties."""
        self.image_x = image_x
        """float: x coordinate of the upper left corner"""
        self.image_y = image_y
        """float: y coordinate of the upper left corner"""
        self.height = height
        """float: height of the image"""
        self.width = width
        """float: width of the image"""


class ImageFile:
    """Contains the properties for a thermal map image file."""

    def __init__(
        self,
        board_bounds: BoardBounds,
        coordinate_units: str,
        image_bounds: ImageBounds,
        legend_bounds: "LegendBounds",
        legend_orientation: "LegendOrientation",
        max_temperature: float,
        max_temperature_units: str,
        min_temperature: float,
        min_temperature_units: str,
    ):
        """Initialize the thermal image file properties."""
        self.board_bounds = board_bounds
        """BoardBounds: board_bounds"""
        self.coordinate_units = coordinate_units
        """str: coordinate_units"""
        self.image_bounds = image_bounds
        """ImageBounds: image_bounds"""
        self.legend_bounds = legend_bounds
        """LegendBounds: legend_bounds"""
        self.legend_orientation = legend_orientation
        """LegendOrientation: legend_orientation"""
        self.max_temperature = max_temperature
        """float: max_temperature"""
        self.max_temperature_units = max_temperature_units
        """str: max_temperature_units"""
        self.min_temperature = min_temperature
        """float: min_temperature"""
        self.min_temperature_units = min_temperature_units
        """str: min_temperature_units"""


class LegendBounds:
    """Contains the properties of the legend bounds."""

    def __init__(self, legend_x: float, legend_y: float, height: float, width: float):
        """Initialize the legend bounds properties."""
        self.legend_x = legend_x
        """float: x coordinate of the upper left corner"""
        self.legend_y = legend_y
        """float: y coordinate of the upper left corner"""
        self.height = height
        """float: height of the legend"""
        self.width = width
        """float: width of the legend"""


class LegendOrientation:
    """Constants for legend orientation in the update thermal maps request."""

    __legend_orientation = thermal_map_file.ImageFile.LegendOrientation
    HORIZONTAL = __legend_orientation.Horizontal
    "Horizontal"
    VERTICAL = __legend_orientation.Vertical
    "Vertical"


class ThermalBoardSide:
    """Constants for thermal board side in the update thermal maps request."""

    BOTTOM = thermal_map_file.ThermalBoardSide.Bottom
    "Bottom"
    BOTH = thermal_map_file.ThermalBoardSide.Both
    "Both"
    TOP = thermal_map_file.ThermalBoardSide.Top
    "Top"


class ThermalMapsFileType:
    """Constants for File Type in the Update Thermal Maps request."""

    CSV = thermal_map_file.FileType.CSV
    "CSV"
    EXCEL = thermal_map_file.FileType.Excel
    "Excel"
    IMAGE = thermal_map_file.FileType.Image
    "Image"
    TMAP = thermal_map_file.FileType.TMAP
    "Icepak Thermal Map (.TMAP)"


class StrainMapsFileType:
    """Constants for File Type in the Add Strain Maps request."""

    CSV = add_strain_map_request.StrainMapFile.FileType.CSV
    "CSV"
    EXCEL = add_strain_map_request.StrainMapFile.FileType.Excel
    "Excel"
    IMAGE = add_strain_map_request.StrainMapFile.FileType.Image
    "Image"


class StrainMapLegendOrientation:
    """Constants for legend orientation in the add strain maps request."""

    __legend_orientation = add_strain_map_request.StrainMapFile.StrainMapImageFile.LegendOrientation
    HORIZONTAL = __legend_orientation.Horizontal
    "Horizontal"
    VERTICAL = __legend_orientation.Vertical
    "Vertical"
