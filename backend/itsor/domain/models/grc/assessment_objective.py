from dataclasses import dataclass, field

from itsor.domain._ulid import typed_ulid_factory


def _normalize_required_text(value: str, field_name: str) -> str:
	if not isinstance(value, str):
		raise ValueError(f"{field_name} must be a string")
	normalized = value.strip()
	if not normalized:
		raise ValueError(f"{field_name} is required")
	return normalized


@dataclass
class AssessmentObjective:
	id: str = field(default_factory=typed_ulid_factory(str), init=False)
	control_id: str = ""
	description: str = ""

	def __post_init__(self) -> None:
		self.control_id = _normalize_required_text(self.control_id, "control_id")
		self.description = _normalize_required_text(self.description, "description")


__all__ = ["AssessmentObjective"]