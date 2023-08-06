from typing import Any, Dict, Tuple, Type, Union

import pydantic
from pydantic import BaseConfig, Field, root_validator
from pydantic.fields import FieldInfo, ModelField
from typing_extensions import Literal


class DiscriminatedFieldInfo(FieldInfo):
    @staticmethod
    def _get_field_info(
        field_name: str, annotation: Any, value: Any, config: Type["BaseConfig"]
    ) -> Tuple["DiscriminatedFieldInfo", Any]:
        return cls._get_field_info(field_name=field_name, annotation=annotation, value=value, config=config)

    # def __init__(self, field_info: FieldInfo, discriminator: str) -> None:
    #     self._field_info = field_info
    #     self._discriminator = discriminator


def discriminated_field(*args: Any, discriminator: str, **kwargs: Any) -> Any:
    field_info = Field(*args, **kwargs)
    return DiscriminatedFieldInfo(field_info=field_info, discriminator=discriminator)


# class DiscriminatedUnion:
#     @classmethod
#     def __get_validators(cls) -> Generator[Callable]:
#         yield cls.validate

#     @classmethod
#     def validate(cls, v: Any) -> Any:


class TimeSeries(pydantic.BaseModel):
    node_type: Literal["TimeSeries"]
    meows: int


class Operation(pydantic.BaseModel):
    node_type: Literal["Operation"]
    arfs: float


class NodeContainer(pydantic.BaseModel):
    node: Union[TimeSeries, Operation]  # = discriminated_field(..., discriminator="node_type")

    class Config:
        extra = pydantic.Extra.forbid

        discriminator = "node_type"
        discriminated_field = "node"

        @classmethod
        def prepare_field(cls, field: "ModelField") -> None:
            print(field)

        @classmethod
        def get_field_info(cls, name: str) -> Dict[str, Any]:
            return {}

    @root_validator(pre=True)
    def check_discriminator_present(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        discrim_field = cls.Config.discriminated_field
        assert discrim_field in values, f"missing discriminated field {discrim_field}"
        discrim_value = values[discrim_field]
        assert cls.Config.discriminator in discrim_value
        return values


NodeContainer(node={"node_type": "TimeSeries", "meows": 4})
NodeContainer(node={"node_type": "Operation", "meows": 4})
NodeContainer(node={"node_type": "TimeSeries", "arfs": 3.141596525837})
NodeContainer(node={"meows": 4})
NodeContainer(node={"random": "information"})
