from datetime import datetime

from pydantic import BaseModel


class ItamReportMetadata(BaseModel):
    report_id: str
    safeguard_id: str
    as_of: datetime
    generated_at: datetime
    query_version: str


class ItamReportSummary(BaseModel):
    total_evaluated: int
    total_non_compliant: int
    compliance_rate: float


class ItamReportRow(BaseModel):
    resource_id: str
    resource_type: str
    reason: str


class ItamReportException(BaseModel):
    exception_id: str
    exception_expires_at: datetime | None = None
    reason: str


class ItamReportEvidenceLink(BaseModel):
    evidence_record_id: str
    source_system: str


class ItamSafeguardReportResponse(BaseModel):
    metadata: ItamReportMetadata
    summary: ItamReportSummary
    rows: list[ItamReportRow]
    exceptions: list[ItamReportException]
    evidence_links: list[ItamReportEvidenceLink]
