import enum
from typing import Mapping, NamedTuple, Optional

from myst.connectors.source_connectors import cleaned_observations, enhanced_forecast, historical_hourly_conditions
from myst.core.time.time_delta import TimeDelta
from myst.models.types import AxisLabels, CoordinateLabels, Shape
from myst.recipes.time_series_recipes.time_series_recipe import TimeSeriesRecipe
from myst.resources.layer import Layer
from myst.resources.project import Project
from myst.resources.source import Source
from myst.resources.time_series import TimeSeries

_HISTORICAL_APIS_CUTOVER_BOUNDARY = TimeDelta("-PT23H")
_HISTORICAL_TO_FORECAST_CUTOVER_BOUNDARY = TimeDelta("PT1H")


@enum.unique
class Field(enum.Enum):
    TEMPERATURE = enum.auto()
    RELATIVE_HUMIDITY = enum.auto()
    WIND_DIRECTION = enum.auto()
    WIND_SPEED = enum.auto()


_CLEANED_OBSERVATIONS_FIELD_MAPPINGS: Mapping[Field, cleaned_observations.Field] = {
    Field.TEMPERATURE: cleaned_observations.Field.SURFACE_TEMPERATURE_CELSIUS,
    Field.RELATIVE_HUMIDITY: cleaned_observations.Field.RELATIVE_HUMIDITY_PERCENT,
    Field.WIND_DIRECTION: cleaned_observations.Field.WIND_DIRECTION_DEGREES,
    Field.WIND_SPEED: cleaned_observations.Field.WIND_SPEED_MPH,
}
_HISTORICAL_HOURLY_CONDITIONS_FIELD_MAPPINGS: Mapping[Field, historical_hourly_conditions.Field] = {
    Field.TEMPERATURE: historical_hourly_conditions.Field.TEMPERATURE,
    Field.RELATIVE_HUMIDITY: historical_hourly_conditions.Field.RELATIVE_HUMIDITY,
    Field.WIND_DIRECTION: historical_hourly_conditions.Field.WIND_DIRECTION,
    Field.WIND_SPEED: historical_hourly_conditions.Field.WIND_SPEED,
}
_ENHANCED_FORECAST_FIELD_MAPPINGS = {
    Field.TEMPERATURE: enhanced_forecast.Field.TEMPERATURE,
    Field.RELATIVE_HUMIDITY: enhanced_forecast.Field.RELATIVE_HUMIDITY,
    Field.WIND_DIRECTION: enhanced_forecast.Field.WIND_DIRECTION,
    Field.WIND_SPEED: enhanced_forecast.Field.WIND_SPEED,
    # TODO(sjespersen): Do we need others?
}


class Location(NamedTuple):
    latitude: float
    longitude: float


@enum.unique
class MetarStation(Location, enum.Enum):
    # TODO(sjespersen): Get the right lat/lngs for these!
    KSFO = Location(latitude=37.618331, longitude=-122.378647)
    KSKX = Location(latitude=36.458937, longitude=-105.671378)


class TheWeatherCompany(TimeSeriesRecipe):
    def __init__(self, field: Field, metar_station: MetarStation) -> None:
        self._field = field
        self._metar_station = metar_station

    def create_time_series(
        self,
        project: Project,
        title: str,
        sample_period: TimeDelta,
        cell_shape: Shape = (),
        coordinate_labels: CoordinateLabels = (),
        axis_labels: AxisLabels = (),
        description: Optional[str] = None,
    ) -> TimeSeries:
        latitude = self._metar_station.latitude
        longitude = self._metar_station.longitude
        cleaned_observations_source = Source.create(
            project=project,
            title=f"Cleaned Observations ({self._metar_station.name})",
            connector=cleaned_observations.CleanedObservations(
                latitude=latitude, longitude=longitude, fields=[_CLEANED_OBSERVATIONS_FIELD_MAPPINGS[self._field]]
            ),
        )
        historical_hourly_conditions_source = Source.create(
            project=project,
            title=f"Historical Hourly Conditions ({self._metar_station.name})",
            connector=historical_hourly_conditions.HistoricalHourlyConditions(
                latitude=latitude,
                longitude=longitude,
                fields=[_HISTORICAL_HOURLY_CONDITIONS_FIELD_MAPPINGS[self._field]],
            ),
        )
        enhanced_forecast_source = Source.create(
            project=project,
            title=f"Enhanced Forecast ({self._metar_station.name})",
            connector=enhanced_forecast.EnhancedForecast(
                latitude=latitude, longitude=longitude, fields=[_ENHANCED_FORECAST_FIELD_MAPPINGS[self._field]]
            ),
        )
        time_series = TimeSeries.create(
            project=project,
            title=title,
            sample_period=sample_period,
            cell_shape=cell_shape,
            coordinate_labels=coordinate_labels,
            axis_labels=axis_labels,
            description=description,
        )
        Layer.create(
            downstream_node=time_series,
            upstream_node=cleaned_observations_source,
            order=0,
            output_index=0,
            label_indexer=_CLEANED_OBSERVATIONS_FIELD_MAPPINGS[self._field],
            end_timing=_HISTORICAL_APIS_CUTOVER_BOUNDARY,
        )
        Layer.create(
            downstream_node=time_series,
            upstream_node=historical_hourly_conditions_source,
            order=1,
            output_index=0,
            label_indexer=_HISTORICAL_HOURLY_CONDITIONS_FIELD_MAPPINGS[self._field],
            start_timing=_HISTORICAL_APIS_CUTOVER_BOUNDARY,
            end_timing=_HISTORICAL_TO_FORECAST_CUTOVER_BOUNDARY,
        )
        Layer.create(
            downstream_node=time_series,
            upstream_node=enhanced_forecast_source,
            order=2,
            output_index=0,
            label_indexer=_ENHANCED_FORECAST_FIELD_MAPPINGS[self._field],
            start_timing=_HISTORICAL_TO_FORECAST_CUTOVER_BOUNDARY,
        )
        return time_series
