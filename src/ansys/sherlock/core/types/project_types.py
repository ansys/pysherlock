# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Project Service."""

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ValidationInfo, field_validator

from ansys.sherlock.core.types.common_types import (
    basic_list_str_validator,
    basic_str_validator,
    optional_str_validator,
)

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

    def __init__(
        self,
        temperature_offset: float,
        temperature_offset_units: str,
    ):
        """Initialize the thermal map Icepak file properties."""
        self.temperature_offset = temperature_offset
        """float: temperature_offset"""
        self.temperature_offset_units = temperature_offset_units
        """str: temperature_offset_units"""


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


class ImportGDSIIRequest(BaseModel):
    """Contains the information to import a GDSII project file and any optional config files."""

    gdsii_file: str
    """Full path to the GDSII file (.gds, .sf, or .strm) to be imported."""

    technology_file: Optional[str] = None
    """Full path to the optional technology file (.xml, .tech, or .layermap) to be imported."""

    layer_map_file: Optional[str] = None
    """Full path to the optional layer map file (.map) to be imported."""

    project: Optional[str] = None
    """Sherlock project name. If empty, the filename will be used for the project name."""

    cca_name: Optional[str] = None
    """Project CCA name. If empty, the filename will be used for the CCA name."""

    guess_part_properties: Optional[bool] = False
    """Option to guess part properties."""

    polyline_simplification_enabled: Optional[bool] = False
    """Option to enable polyline simplification."""

    polyline_tolerance: Optional[float] = 0.0
    """Polyline simplification tolerance, if enabled."""

    polyline_tolerance_units: Optional[str] = None
    """Polyline simplification tolerance units, if enabled."""

    @field_validator("gdsii_file", "technology_file", "layer_map_file")
    @classmethod
    def str_validation(cls, value: Optional[str], info):
        """Validate string fields listed."""
        if value is None or value.strip() == "":
            raise ValueError(f"{info.field_name} is invalid because it is None or empty.")
        return basic_str_validator(value, info.field_name)

    @field_validator("project", "cca_name")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow empty strings for project and cca_name."""
        return optional_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> project_service.ImportGDSIIRequest:
        return project_service.ImportGDSIIRequest(
            gdsiiFile=self.gdsii_file,
            technologyFile=self.technology_file or "",
            layerMapFile=self.layer_map_file or "",
            project=self.project or "",
            ccaName=self.cca_name or "",
            guessPartProperties=self.guess_part_properties,
            polylineSimplificationEnabled=self.polyline_simplification_enabled,
            polylineTolerance=self.polyline_tolerance,
            polylineToleranceUnits=self.polyline_tolerance_units or "",
        )


class OutlineFileType(Enum):
    """Constants for File Type in the Update Outline request."""

    CSV_EXCEL = project_service.OutlineFile.FileType.CsvExcel
    "CSV Excel"
    GERBER = project_service.OutlineFile.FileType.Gerber
    "Gerber"
    IPC2581 = project_service.OutlineFile.FileType.IPC2581
    "IPC2581"


class CsvExcelOutlineFile(BaseModel):
    """Contains the properties for a CSV or Excel outline file."""

    header_row_count: int
    """Number of rows before the column header in the file"""
    x_location_column: str
    """X location column name"""
    y_location_column: str
    """Y location column name"""
    location_units: str
    """Units for location values"""

    def _convert_to_grpc(self) -> project_service.OutlineFile.CsvExcelOutlineFile:
        return project_service.OutlineFile.CsvExcelOutlineFile(
            headerRowCount=self.header_row_count,
            xLocationColumn=self.x_location_column,
            yLocationColumn=self.y_location_column,
            locationUnits=self.location_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator("x_location_column", "y_location_column", "location_units")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class GerberOutlineFile(BaseModel):
    """Contains the properties for a Gerber outline file."""

    parse_decimal_first: bool = False
    """Indicates to parse decimals based on the length of the format specifier."""

    def _convert_to_grpc(self) -> project_service.OutlineFile.GerberOutlineFile:
        return project_service.OutlineFile.GerberOutlineFile(
            parseDecimalFirst=self.parse_decimal_first,
        )


class OutlineFile(BaseModel):
    """Contains the properties for an outline file."""

    file_name: str
    """The filename of the outline file."""
    file_comment: Optional[str] = None
    """The comment for the outline file."""
    file_type: OutlineFileType
    """The type of outline file."""
    outline_file_data: Optional[Union[CsvExcelOutlineFile, GerberOutlineFile]] = None
    """Specific outline file type properties"""
    cca_names: list[str]
    """The list of CCA names for the outline file."""

    def _convert_to_grpc(self) -> project_service.OutlineFile:
        grpc_outline_file = project_service.OutlineFile()

        grpc_outline_file.fileName = self.file_name

        if self.file_comment is not None:
            grpc_outline_file.fileComment = self.file_comment

        grpc_outline_file.fileType = self.file_type.value

        grpc_outline_file.cca.extend(self.cca_names)

        if self.file_type == OutlineFileType.CSV_EXCEL:
            if self.outline_file_data is None or not isinstance(
                self.outline_file_data, CsvExcelOutlineFile
            ):
                raise ValueError(
                    "CsvExcel file outline file data is required for CSV Excel outline files."
                )

            grpc_outline_file.csvExcelFile.CopyFrom(self.outline_file_data._convert_to_grpc())

        elif self.file_type == OutlineFileType.GERBER and (
            self.outline_file_data is None
            or not isinstance(self.outline_file_data, GerberOutlineFile)
        ):
            raise ValueError("Gerber file outline file data is required for Gerber outline files.")

            grpc_outline_file.gerberFile.CopyFrom(self.outline_file_data._convert_to_grpc())

        return grpc_outline_file

    @field_validator("file_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("file_comment")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow empty strings for file_comment."""
        return optional_str_validator(value, info.field_name)

    @field_validator("cca_names")
    @classmethod
    def validate_non_empty_cca_names(cls, value: list[str], info: ValidationInfo):
        """Validate cca_names contains at least one name and none are empty."""
        return basic_list_str_validator(value, info.field_name)


class AddOutlineFileRequest(BaseModel):
    """Contains the information to add outline files to a project."""

    project: str
    """Sherlock project name."""
    outline_files: list[OutlineFile]
    """List of outline files to add."""

    def _convert_to_grpc(self) -> project_service.AddOutlineFileRequest:
        if not self.outline_files:
            raise ValueError("At least one outline file is required.")

        request = project_service.AddOutlineFileRequest()
        request.project = self.project
        for outline_file in self.outline_files:
            request.outlineFiles.append(outline_file._convert_to_grpc())
        return request

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class CopperGerberFile(BaseModel):
    """Properties specific to a Gerber copper file."""

    parse_decimal_first_enabled: Optional[bool] = False
    """Whether to parse decimal values before other formats in the Gerber file."""


class CopperImageFile(BaseModel):
    """Properties specific to an image-based copper file."""

    image_type: Optional[project_service.CopperFile.ImageType.ValueType] = (
        project_service.CopperFile.ImageType.Background
    )
    """Indicates whether the image represents a background or foreground layer."""

    image_color: Optional[str] = ""
    """Optional color description or label for the image (e.g., 'black', 'white')."""

    """Allow non-standard types like Protobuf enums in Pydantic models."""
    model_config = {"arbitrary_types_allowed": True}


class CopperFile(BaseModel):
    """Metadata and options for a copper file to be imported into a project."""

    file_name: str
    """The name of the file being imported."""

    file_type: Optional[project_service.CopperFile.FileType.ValueType] = (
        project_service.CopperFile.FileType.EDB
    )
    """The format/type of the copper file (e.g., Gerber, ODB++, IPC2581)."""

    file_comment: Optional[str] = ""
    """Optional comment or description for the copper file."""

    copper_layer: str
    """The name of the copper layer this file is associated with."""

    polarity: Optional[project_service.CopperFile.Polarity.ValueType] = (
        project_service.CopperFile.Polarity.Positive
    )
    """Indicates whether the copper file uses positive or negative polarity."""

    layer_snapshot_enabled: Optional[bool] = False
    """Enable or disable the generation of a layer snapshot for this copper file."""

    cca: List[str] = []
    """List of CCA (circuit card assembly) names associated with this copper file."""

    gerber_file: Optional[CopperGerberFile] = None
    """Optional settings specific to Gerber file import."""

    image_file: Optional[CopperImageFile] = None
    """Optional settings specific to image-based file import."""

    """Allow non-standard types like Protobuf enums in Pydantic models."""
    model_config = {"arbitrary_types_allowed": True}

    def _convert_to_grpc(self) -> project_service.CopperFile:
        copper_file_msg = project_service.CopperFile()
        copper_file_msg.fileName = self.file_name
        copper_file_msg.fileType = self.file_type
        copper_file_msg.fileComment = self.file_comment or ""
        copper_file_msg.copperLayer = self.copper_layer
        copper_file_msg.polarity = self.polarity
        copper_file_msg.layerSnapshotEnabled = self.layer_snapshot_enabled
        copper_file_msg.cca.extend(self.cca)

        if self.gerber_file:
            copper_file_msg.gerberFile.parseDecimalFirstEnabled = (
                self.gerber_file.parse_decimal_first_enabled
            )

        if self.image_file:
            copper_file_msg.imageFile.imageType = self.image_file.image_type
            copper_file_msg.imageFile.imageColor = self.image_file.image_color or ""

        return copper_file_msg


class ImportCopperFile(BaseModel):
    """Representation of a copper file and its associated metadata for import."""

    copper_file: str
    """The path to the copper file being imported."""

    copper_file_properties: CopperFile
    """Metadata and configuration options for this copper file."""

    @field_validator("copper_file")
    @classmethod
    def copper_file_validator(cls, value: str, info):
        """Validate that the file path is not empty."""
        if value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be empty.")
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> project_service.ImportCopperFilesRequest.ImportCopperFile:
        grpc_import_copper_file = project_service.ImportCopperFilesRequest.ImportCopperFile()
        grpc_import_copper_file.copperFile = self.copper_file
        grpc_import_copper_file.copperFileProperties.CopyFrom(
            self.copper_file_properties._convert_to_grpc()
        )
        return grpc_import_copper_file


class ImportCopperFilesRequest(BaseModel):
    """Request to import multiple copper files into a given project."""

    project: str
    """The name of the project into which the copper files will be imported."""

    copper_files: List[ImportCopperFile]
    """List of copper files with metadata to import into the project."""

    @field_validator("project")
    @classmethod
    def project_validator(cls, value: str, info):
        """Validate that the project name is not empty."""
        if value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be empty.")
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> project_service.ImportCopperFilesRequest:
        request = project_service.ImportCopperFilesRequest()
        request.project = self.project
        for copper_file in self.copper_files:
            request.copperFiles.append(copper_file._convert_to_grpc())
        return request
