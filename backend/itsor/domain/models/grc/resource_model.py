from dataclasses import dataclass, field
from urllib.parse import urlparse

from itsor.domain._ulid import typed_ulid_factory


def _normalize_required_text(value: str, field_name: str) -> str:
	if not isinstance(value, str):
		raise ValueError(f"{field_name} must be a string")
	normalized = value.strip()
	if not normalized:
		raise ValueError(f"{field_name} is required")
	return normalized


def _normalize_url(value: str, field_name: str) -> str:
	normalized = _normalize_required_text(value, field_name)
	parsed = urlparse(normalized)
	if parsed.scheme not in {"http", "https"} or not parsed.netloc:
		raise ValueError(f"{field_name} must be a valid http/https URL")
	return normalized


@dataclass
class GrcResource:
	id: str = field(default_factory=typed_ulid_factory(str), init=False)
	title: str = ""
	url: str = ""

	def __post_init__(self) -> None:
		self.title = _normalize_required_text(self.title, "title")
		self.url = _normalize_url(self.url, "url")


__all__ = ["GrcResource"]