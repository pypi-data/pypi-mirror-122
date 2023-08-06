from abc import ABC, abstractmethod
from typing import Optional

from myst.core.time.time_delta import TimeDelta
from myst.models.types import AxisLabels, CoordinateLabels, Shape
from myst.resources.project import Project
from myst.resources.time_series import TimeSeries


class TimeSeriesRecipe(ABC):
    @abstractmethod
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
        raise NotImplementedError()
