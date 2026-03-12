from typing import Any, Literal

from pydantic import BaseModel, Field


OscalDocumentType = Literal[
    "catalog",
    "profile",
    "mapping",
    "assessment-plan",
    "assessment-results",
    "poam",
    "component-definition",
    "system-security-plan",
]


class OscalDocumentCreate(BaseModel):
    document_type: OscalDocumentType
    content_json: dict[str, Any] = Field(alias="content")
    title: str | None = None


class OscalDocumentReplace(BaseModel):
    document_type: OscalDocumentType
    content_json: dict[str, Any] = Field(alias="content")
    title: str | None = None


class OscalDocumentResponse(BaseModel):
    id: str
    document_type: str
    content_json: dict[str, Any] = Field(alias="content")
    title: str | None = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class OscalSubmoduleUpsert(BaseModel):
    content_json: dict[str, Any] = Field(alias="content")
    title: str | None = None
