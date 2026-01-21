# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Lifecycle Service."""

from typing import Optional

from pydantic import BaseModel, ValidationInfo, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator, optional_str_validator

try:
    import SherlockLifeCycleService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2


class HarmonicVibeProfileCsvFileProperties(BaseModel):
    """Properties of a harmonic vibe profile CSV file."""

    profile_name: str
    """Name of the harmonic vibe profile."""
    header_row_count: int
    """Number of rows before the column header in the file."""
    column_delimiter: str = ","
    """Delimiter used to separate columns in the file."""
    numeric_format: str = None
    """Numeric format for the values."""
    frequency_column: str
    """Name of the column containing frequency values."""
    frequency_units: str
    """Units of the frequency values"""
    load_column: str
    """Name of the column containing load values."""
    load_units: str
    """Units of the load values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.LoadHarmonicProfileRequest.CSVProps:
        """Convert to gRPC CVSProps."""
        return SherlockLifeCycleService_pb2.LoadHarmonicProfileRequest.CSVProps(
            profileName=self.profile_name,
            headerRowNumber=self.header_row_count,
            columnDelim=self.column_delimiter,
            numericFormat=self.numeric_format,
            freqColumn=self.frequency_column,
            freqUnits=self.frequency_units,
            loadColumn=self.load_column,
            loadUnits=self.load_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator(
        "profile_name", "frequency_column", "frequency_units", "load_column", "load_units"
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("column_delimiter", "numeric_format")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)


class RandomVibeProfileCsvFileProperties(BaseModel):
    """Properties of a random vibe profile CSV file."""

    profile_name: str
    """Name of the random vibe profile."""
    header_row_count: int
    """Number of rows before the column header in the file."""
    column_delimiter: str = ","
    """Delimiter used to separate columns in the file."""
    numeric_format: str = None
    """Numeric format for the values."""
    frequency_column: str
    """Name of the column containing frequency values."""
    frequency_units: str
    """Units of the frequency values"""
    amplitude_column: str
    """Name of the column containing amplitude values."""
    amplitude_units: str
    """Units of the amplitude values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.LoadRandomVibeProfileRequest.CSVProps:
        """Convert to gRPC CVSProps."""
        return SherlockLifeCycleService_pb2.LoadRandomVibeProfileRequest.CSVProps(
            profileName=self.profile_name,
            headerRowNumber=self.header_row_count,
            columnDelim=self.column_delimiter,
            numericFormat=self.numeric_format,
            freqColumn=self.frequency_column,
            freqUnits=self.frequency_units,
            amplColumn=self.amplitude_column,
            amplUnits=self.amplitude_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator(
        "profile_name", "frequency_column", "frequency_units", "amplitude_column", "amplitude_units"
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("column_delimiter", "numeric_format")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)


class ShockProfileDatasetCsvFileProperties(BaseModel):
    """Properties of a shock event profile using dataset CSV file."""

    profile_name: str
    """Name of the shock vibe profile."""
    header_row_count: int
    """Number of rows before the column header in the file."""
    column_delimiter: str = ","
    """Delimiter used to separate columns in the file."""
    numeric_format: str = None
    """Numeric format for the values."""
    time_column: str
    """Name of the column containing timeuency values."""
    time_units: str
    """Units of the timeuency values"""
    load_column: str
    """Name of the column containing load values."""
    load_units: str
    """Units of the load values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.LoadShockProfileDatasetRequest.CSVProps:
        """Convert to gRPC CVSProps."""
        return SherlockLifeCycleService_pb2.LoadShockProfileDatasetRequest.CSVProps(
            profileName=self.profile_name,
            headerRowNumber=self.header_row_count,
            columnDelim=self.column_delimiter,
            numericFormat=self.numeric_format,
            timeColumn=self.time_column,
            timeUnits=self.time_units,
            loadColumn=self.load_column,
            loadUnits=self.load_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator("profile_name", "time_column", "time_units", "load_column", "load_units")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("column_delimiter", "numeric_format")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)


class ShockProfilePulsesCsvFileProperties(BaseModel):
    """Properties of a shock event profile using pulses CSV file."""

    profile_name: str
    """Name of the shock vibe profile."""
    header_row_count: int
    """Number of rows before the column header in the file."""
    column_delimiter: str = ","
    """Delimiter used to separate columns in the file."""
    numeric_format: str = None
    """Numeric format for the values."""
    duration: float
    """Pulse duration length"""
    duration_units: str
    """Time units of the pulse duration"""
    sample_rate: float
    """Sample rate"""
    sample_rate_units: str
    """Time units of the sample rate"""
    shape_column: str
    """Name of the column containing shape values."""
    load_column: str
    """Name of the column containing load values."""
    load_units: str
    """Units of the load values."""
    frequency_column: str
    """Name of the column containing frequency values."""
    frequency_units: str
    """Units of the frequency values"""
    decay_column: str
    """Name of the column containing decay values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.LoadShockProfilePulsesRequest.CSVProps:
        """Convert to gRPC CVSProps."""
        return SherlockLifeCycleService_pb2.LoadShockProfilePulsesRequest.CSVProps(
            profileName=self.profile_name,
            headerRowNumber=self.header_row_count,
            columnDelim=self.column_delimiter,
            numericFormat=self.numeric_format,
            duration=self.duration,
            durationUnits=self.duration_units,
            sampleRate=self.sample_rate,
            sampleRateUnits=self.sample_rate_units,
            shapeColumn=self.shape_column,
            loadColumn=self.load_column,
            loadUnits=self.load_units,
            freqColumn=self.frequency_column,
            freqUnits=self.frequency_units,
            decayColumn=self.decay_column,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator("duration", "sample_rate")
    @classmethod
    def greater_than_zero_float_validation(cls, value: float, info: ValidationInfo):
        """Validate float fields listed contain values greater than 0."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than 0.")
        return value

    @field_validator(
        "profile_name",
        "duration_units",
        "sample_rate_units",
        "shape_column",
        "load_column",
        "load_units",
        "frequency_column",
        "frequency_units",
        "decay_column",
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("column_delimiter", "numeric_format")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)


class ThermalProfileCsvFileProperties(BaseModel):
    """Properties of a thermal profile CSV file."""

    profile_name: str
    """Name of the thermal profile."""
    header_row_count: int
    """Number of rows before the column header in the file."""
    column_delimiter: str = ","
    """Delimiter used to separate columns in the file."""
    numeric_format: str = None
    """Numeric format for the values."""
    step_column: str
    """Name of the column containing step values."""
    type_column: str
    """Name of the column containing step type values."""
    time_column: str
    """Name of the column containing time duration values."""
    time_units: str
    """Units of the time values."""
    temperature_column: str
    """Name of the column containing temperature values."""
    temperature_units: str
    """Units of the temperature values."""

    def _convert_to_grpc(
        self,
    ) -> SherlockLifeCycleService_pb2.LoadThermalProfileRequest.CSVProps:
        """Convert to gRPC CVSProps."""
        return SherlockLifeCycleService_pb2.LoadThermalProfileRequest.CSVProps(
            profileName=self.profile_name,
            headerRowNumber=self.header_row_count,
            columnDelim=self.column_delimiter,
            numericFormat=self.numeric_format,
            stepColumn=self.step_column,
            typeColumn=self.type_column,
            timeColumn=self.time_column,
            timeUnits=self.time_units,
            tempColumn=self.temperature_column,
            tempUnits=self.temperature_units,
        )

    @field_validator("header_row_count")
    @classmethod
    def non_negative_int_validation(cls, value: int, info: ValidationInfo):
        """Validate integer fields listed contain non-negative values."""
        if value < 0:
            raise ValueError(f"{info.field_name} must be greater than or equal to 0.")
        return value

    @field_validator(
        "profile_name",
        "step_column",
        "type_column",
        "time_column",
        "time_units",
        "temperature_column",
        "temperature_units",
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("column_delimiter", "numeric_format")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)


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
    number_of_range_bins: int
    """Number of range bins for binning cycles, 0 for no range binning."""
    number_of_mean_bins: int
    """Number of mean bins for binning cycles, 0 for no mean binning."""
    number_of_dwell_bins: int
    """Number of dwell bins for binning cycles, 0 for no dwell binning."""
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

    @field_validator("number_of_range_bins", "number_of_mean_bins", "number_of_dwell_bins")
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
            numberOfRangeBins=self.number_of_range_bins,
            numberOfMeanBins=self.number_of_mean_bins,
            numberOfDwellBins=self.number_of_dwell_bins,
            temperatureRangeFilteringLimit=self.temperature_range_filtering_limit,
            timeFilteringLimit=self.time_filtering_limit,
            timeFilteringLimitUnits=self.time_filtering_limit_units,
            generatedCyclesLabel=self.generated_cycles_label,
        )


class UpdateLifeCycleRequest(BaseModel):
    """Request to update the life cycle."""

    project: str
    """Sherlock project name."""

    new_name: str
    """The new name of the life cycle."""

    new_description: str
    """The new description of the life cycle."""

    new_reliability_metric: float
    """The new reliability metric value.
    Options are: "Reliability (%)", "Prob. of Failure (%)",
    "MTBF (years)", "MTBF (hours)", "FITs (1E6 hrs)", "FITs (1E9 hrs)"
    """

    new_reliability_metric_units: str
    """The new reliability metric units."""

    new_service_life: float
    """The new service life value."""

    new_service_life_units: str
    """The new service life units.
    Options are: "year", "day", "hr", "min", "sec"
    """

    result_archive_file_name: str
    """File name for saved results. File names will be overwritten.
       Sub-Assembly results will be saved."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.UpdateLifeCycleRequest:
        """Convert to gRPC SaveHarmonicProfileRequest."""
        return SherlockLifeCycleService_pb2.UpdateLifeCycleRequest(
            project=self.project,
            newName=self.new_name,
            newDescription=self.new_description,
            newReliabilityMetric=self.new_reliability_metric,
            newReliabilityMetricUnits=self.new_reliability_metric_units,
            newServiceLife=self.new_service_life,
            newServiceLifeUnits=self.new_service_life_units,
            resultArchiveFileName=self.result_archive_file_name,
        )


class SaveHarmonicProfileRequest(BaseModel):
    """Request to save a harmonic life cycle event profile to a .dat or .csv file."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """The name of the life cycle phase this event is associated with."""

    event_name: str
    """Harmonic event name."""

    triaxial_axis: str | None = None
    """If the harmonic profile type is 'Triaxial', the axis this profile should be assigned to.
    Valid values are: x, y, z.
    """

    file_path: str
    """Full destination path for the .dat or .csv file."""

    @field_validator("project", "phase_name", "event_name", "file_path", "triaxial_axis")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.SaveHarmonicProfileRequest:
        """Convert to gRPC SaveHarmonicProfileRequest."""
        return SherlockLifeCycleService_pb2.SaveHarmonicProfileRequest(
            project=self.project,
            phaseName=self.phase_name,
            eventName=self.event_name,
            triaxialAxis=self.triaxial_axis or "",
            filePath=self.file_path,
        )


class SaveRandomVibeProfileRequest(BaseModel):
    """Request to save a random vibe life cycle event profile to a .dat or .csv file."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """The name of the life cycle phase this event is associated with."""

    event_name: str
    """Random vibe event name."""

    file_path: str
    """Full destination path for the .dat or .csv file."""

    @field_validator("project", "phase_name", "event_name", "file_path")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.SaveRandomVibeProfileRequest:
        """Convert to gRPC SaveRandomVibeProfileRequest."""
        return SherlockLifeCycleService_pb2.SaveRandomVibeProfileRequest(
            project=self.project,
            phaseName=self.phase_name,
            eventName=self.event_name,
            filePath=self.file_path,
        )


class SaveShockPulseProfileRequest(BaseModel):
    """Request to save a shock pulse life cycle event profile to a .dat or .csv file."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """The name of the life cycle phase this event is associated with."""

    event_name: str
    """Shock event name."""

    file_path: str
    """Full destination path for the .dat or .csv file."""

    @field_validator("project", "phase_name", "event_name", "file_path")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.SaveShockPulseProfileRequest:
        """Convert to gRPC SaveShockPulseProfileRequest."""
        return SherlockLifeCycleService_pb2.SaveShockPulseProfileRequest(
            project=self.project,
            phaseName=self.phase_name,
            eventName=self.event_name,
            filePath=self.file_path,
        )


class SaveThermalProfileRequest(BaseModel):
    """Request to save a thermal life cycle event profile to a .dat or .csv file."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """The name of the life cycle phase this event is associated with."""

    event_name: str
    """Thermal event name."""

    file_path: str
    """Full destination path for the .dat or .csv file."""

    @field_validator("project", "phase_name", "event_name", "file_path")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.SaveThermalProfileRequest:
        """Convert to gRPC SaveThermalProfileRequest."""
        return SherlockLifeCycleService_pb2.SaveThermalProfileRequest(
            project=self.project,
            phaseName=self.phase_name,
            eventName=self.event_name,
            filePath=self.file_path,
        )


class DeleteEventRequest(BaseModel):
    """Request to delete a life cycle event from a project phase."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """The name of the life cycle phase from which to delete this event."""

    event_name: str
    """Name of the event to be deleted."""

    @field_validator("project", "phase_name", "event_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.DeleteEventRequest:
        """Convert to gRPC DeleteEventRequest."""
        return SherlockLifeCycleService_pb2.DeleteEventRequest(
            project=self.project,
            phaseName=self.phase_name,
            eventName=self.event_name,
        )


class DeletePhaseRequest(BaseModel):
    """Request to delete a life cycle phase from a project."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """Name of the life cycle phase to be deleted."""

    @field_validator("project", "phase_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.DeletePhaseRequest:
        """Convert to gRPC DeletePhaseRequest."""
        return SherlockLifeCycleService_pb2.DeletePhaseRequest(
            project=self.project,
            phaseName=self.phase_name,
        )


class UpdateLifePhaseRequest(BaseModel):
    """Request for updating an existing life phase in a specified project's life cycle."""

    project: str
    """Sherlock project name."""

    phase_name: str
    """Name of the life cycle phase to be updated."""

    new_phase_name: Optional[str] = None
    """(Optional) Updated name of life phase."""

    new_description: Optional[str] = None
    """(Optional) Updated description of life phase."""

    new_duration: Optional[float] = None
    """(Optional) Updated event duration length."""

    new_duration_units: Optional[str] = None
    """(Optional) Updated event duration units."""

    new_num_of_cycles: Optional[float] = None
    """(Optional) Updated number of cycles defined for the life phase."""

    new_cycle_type: Optional[str] = None
    """(Optional) Updated cycle type. Acceptable values are COUNT, DUTY_CYCLE, PER YEAR, PER DAY,
        PER HOUR, PER MIN, and PER SEC.
    """

    result_archive_file_name: Optional[str] = None
    """(Optional) Filename for saving analysis results and life cycle data, including any
        sub-assembly results. Any existing results will be overwritten. If this file name is
        omitted, then analysis results will not be saved during the update.
    """

    @field_validator("project", "phase_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator(
        "new_phase_name",
        "new_description",
        "new_duration_units",
        "new_cycle_type",
        "result_archive_file_name",
    )
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the optional fields to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLifeCycleService_pb2.UpdateLifePhaseRequest:
        request = SherlockLifeCycleService_pb2.UpdateLifePhaseRequest()
        request.project = self.project
        request.phaseName = self.phase_name
        if self.new_phase_name is not None:
            request.newPhaseName = self.new_phase_name
        if self.new_description is not None:
            request.newDescription = self.new_description
        if self.new_duration is not None:
            request.newDuration = self.new_duration
        if self.new_duration_units is not None:
            request.newDurationUnits = self.new_duration_units
        if self.new_num_of_cycles is not None:
            request.newNumOfCycles = self.new_num_of_cycles
        if self.new_cycle_type is not None:
            request.newCycleType = self.new_cycle_type
        if self.result_archive_file_name is not None:
            request.resultArchiveFileName = self.result_archive_file_name
        return request
