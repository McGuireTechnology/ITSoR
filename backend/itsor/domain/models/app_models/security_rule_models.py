from __future__ import annotations

from dataclasses import dataclass, field

import ulid

from itsor.domain.ids import SecurityRuleId, TableId


@dataclass
class SecurityRule:
	id: SecurityRuleId = field(default_factory=lambda: SecurityRuleId(str(ulid.new())), init=False)
	table_id: TableId
	filter_expression: str

	def __post_init__(self) -> None:
		if not self.filter_expression.strip():
			raise ValueError("SecurityRule filter_expression cannot be empty")


__all__ = ["SecurityRule"]
