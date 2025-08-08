# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Lifecycle Service."""

from pydantic import BaseModel, ValidationInfo, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator

try:
    import SherlockLifeCycleService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2


class ThermalSignalFileProperties(BaseModel):
    """Properties of a thermal signal file."""

    header_row_count: int
    """Number of rows before the column header in the file."""
    numeric_format: str
    """Numeric format for the values."""
    column_delimiter: str
    """Delimiter used to separate columns in the file."""
    time_column: str
    """Name of the column containing time values."""
    time_units: str
    """Units of the time values."""
    temperature_column: str
    """Name of the column containing temperature values."""
    temperature_units: str
    """Units of the temperature values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.ImportThermalSignalRequest.ThermalSignalFileProperties:
        """Convert to gRPC ThermalSignalFileProperties."""
        return SherlockLifeCycleService_pb2.ImportThermalSignalRequest.ThermalSignalFileProperties(
            headerRowCount=self.header_row_count,
            numericFormat=self.numeric_format,
            columnDelimiter=self.column_delimiter,
            timeColumn=self.time_column,
            timeUnits=self.time_units,
            temperatureColumn=self.temperature_column,
            temperatureUnits=self.temperature_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator("time_column", "time_units", "temperature_column", "temperature_units")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class ImportThermalSignalRequest(BaseModel):
    """Request to import a thermal signal file."""

    file_name: str
    """The full path to the CSV thermal signal file to be imported."""
    project: str
    """Sherlock project name in which the thermal signal is imported."""
    phase_name: str
    """Name of the phase in which the thermal signal is imported."""
    thermal_signal_file_properties: ThermalSignalFileProperties
    """Properties of the thermal signal file."""
    time_removal: bool
    """Option to indicate that time results with shorter half-cycle durations are removed."""
    load_range_percentage: float
    """Defines the fraction of the range near peaks and valleys considered as a dwell region."""
    number_of_bins: int
    """Number of bins for binning cycles, 0 for no binning."""
    temperature_range_filtering_limit: float
    """Minimum cycle range to include in results, 0 for not filtering."""
    time_filtering_limit: float
    """Maximum cycle time to include in results, default is 72 hours."""
    time_filtering_limit_units: str
    """Units of the time filtering limit."""
    generated_cycles_label: str
    """Label used to define the name of all generated thermal events."""

    @field_validator(
        "file_name", "project", "phase_name", "time_filtering_limit_units", "generated_cycles_label"
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("number_of_bins")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.ImportThermalSignalRequest:
        """Convert to gRPC ImportThermalSignalRequest."""
        return SherlockLifeCycleService_pb2.ImportThermalSignalRequest(
            thermalSignalFile=self.file_name,
            project=self.project,
            phaseName=self.phase_name,
            fileProperties=self.thermal_signal_file_properties._convert_to_grpc(),
            timeRemoval=self.time_removal,
            loadRangePercentage=self.load_range_percentage,
            numberOfBins=self.number_of_bins,
            temperatureRangeFilteringLimit=self.temperature_range_filtering_limit,
            timeFilteringLimit=self.time_filtering_limit,
            timeFilteringLimitUnits=self.time_filtering_limit_units,
            generatedCyclesLabel=self.generated_cycles_label,
        )
