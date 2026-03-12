from typing import NewType

OscalCatalogId = NewType("OscalCatalogId", str)
OscalProfileId = NewType("OscalProfileId", str)
OscalMappingCollectionId = NewType("OscalMappingCollectionId", str)
OscalMappingId = NewType("OscalMappingId", str)
OscalComponentDefinitionId = NewType("OscalComponentDefinitionId", str)
OscalAssessmentPlanId = NewType("OscalAssessmentPlanId", str)
OscalAssessmentResultsId = NewType("OscalAssessmentResultsId", str)
OscalAssessmentResultId = NewType("OscalAssessmentResultId", str)
OscalPoamId = NewType("OscalPoamId", str)
OscalPoamItemId = NewType("OscalPoamItemId", str)
OscalSystemSecurityPlanId = NewType("OscalSystemSecurityPlanId", str)

__all__ = [
    "OscalCatalogId",
    "OscalProfileId",
    "OscalMappingCollectionId",
    "OscalMappingId",
    "OscalComponentDefinitionId",
    "OscalAssessmentPlanId",
    "OscalAssessmentResultsId",
    "OscalAssessmentResultId",
    "OscalPoamId",
    "OscalPoamItemId",
    "OscalSystemSecurityPlanId",
]
