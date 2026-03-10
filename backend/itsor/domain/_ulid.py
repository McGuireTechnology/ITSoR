from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

import ulid

TId = TypeVar("TId")


def new_ulid_str() -> str:
	return str(ulid.new())


def typed_ulid_factory(id_type: Callable[[str], TId]) -> Callable[[], TId]:
	def _factory() -> TId:
		return id_type(new_ulid_str())

	return _factory
