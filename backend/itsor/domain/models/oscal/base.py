from dataclasses import is_dataclass

from pydantic import ConfigDict, TypeAdapter
from pydantic.dataclasses import dataclass as pydantic_dataclass


class OscalBaseModel:
	model_config = ConfigDict(extra="forbid", populate_by_name=True)

	def __init_subclass__(cls, **kwargs: object) -> None:
		super().__init_subclass__(**kwargs)
		if not is_dataclass(cls):
			pydantic_dataclass(cls, config=OscalBaseModel.model_config, kw_only=True)

	@classmethod
	def model_validate(cls, payload: object):
		return TypeAdapter(cls).validate_python(payload)

	def model_dump(self, *, by_alias: bool = False, exclude_none: bool = False) -> dict[str, object]:
		return TypeAdapter(type(self)).dump_python(
			self,
			mode="python",
			by_alias=by_alias,
			exclude_none=exclude_none,
		)


class OscalEmptyObject(OscalBaseModel):
	pass


__all__ = ["OscalBaseModel", "OscalEmptyObject"]
