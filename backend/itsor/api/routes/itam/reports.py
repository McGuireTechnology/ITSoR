from datetime import datetime, timezone

from fastapi import APIRouter, Query

from itsor.api.schemas.itam_reports_schemas import (
    ItamReportMetadata,
    ItamReportSummary,
    ItamSafeguardReportResponse,
)

router = APIRouter(prefix="/reports", tags=["itam-reports"])


def _build_stub_report(*, safeguard_id: str, as_of: datetime) -> ItamSafeguardReportResponse:
    return ItamSafeguardReportResponse(
        metadata=ItamReportMetadata(
            report_id=f"{safeguard_id.lower()}-{as_of.strftime('%Y%m%d%H%M%S')}",
            safeguard_id=safeguard_id,
            as_of=as_of,
            generated_at=datetime.now(timezone.utc),
            query_version="v1",
        ),
        summary=ItamReportSummary(
            total_evaluated=0,
            total_non_compliant=0,
            compliance_rate=1.0,
        ),
        rows=[],
        exceptions=[],
        evidence_links=[],
    )


@router.get("/c1/active-asset-inventory", response_model=ItamSafeguardReportResponse)
def c1_active_asset_inventory(
    as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601)."),
):
    return _build_stub_report(safeguard_id="C1-S1", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c1/unmanaged-assets", response_model=ItamSafeguardReportResponse)
def c1_unmanaged_assets(as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601).")):
    return _build_stub_report(safeguard_id="C1-S2", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c1/ownership-gaps", response_model=ItamSafeguardReportResponse)
def c1_ownership_gaps(as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601).")):
    return _build_stub_report(safeguard_id="C1-S3", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c1/stale-assets", response_model=ItamSafeguardReportResponse)
def c1_stale_assets(as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601).")):
    return _build_stub_report(safeguard_id="C1-S5", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c2/observed-software-inventory", response_model=ItamSafeguardReportResponse)
def c2_observed_software_inventory(
    as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601)."),
):
    return _build_stub_report(safeguard_id="C2-S1", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c2/normalization-gaps", response_model=ItamSafeguardReportResponse)
def c2_normalization_gaps(as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601).")):
    return _build_stub_report(safeguard_id="C2-S2", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c2/unauthorized-software", response_model=ItamSafeguardReportResponse)
def c2_unauthorized_software(
    as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601)."),
):
    return _build_stub_report(safeguard_id="C2-S3", as_of=as_of or datetime.now(timezone.utc))


@router.get("/c2/entitlement-shortfall", response_model=ItamSafeguardReportResponse)
def c2_entitlement_shortfall(
    as_of: datetime | None = Query(default=None, description="Report evaluation timestamp (ISO-8601)."),
):
    return _build_stub_report(safeguard_id="C2-S5", as_of=as_of or datetime.now(timezone.utc))
