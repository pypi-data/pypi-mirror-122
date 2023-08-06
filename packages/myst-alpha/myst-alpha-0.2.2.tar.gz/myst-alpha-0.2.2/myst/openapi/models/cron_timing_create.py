from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model


class CronTimingCreate(base_model.BaseModel):
    """Cron timing schema for create requests."""

    object_: Literal["Timing"] = Field(..., alias="object")
    type: Literal["CronTiming"]
    cron_expression: str
    time_zone: Optional[str] = "UTC"
