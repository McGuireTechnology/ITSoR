import pytest

from itsor.domain.models.grc import (
    AssessmentObjective,
    AssetClass,
    Control,
    ControlExample,
    ControlGuidance,
    ControlLink,
    ControlLinkType,
    Domain,
    Framework,
    Frequency,
    GrcResource,
    ImplementationGroup,
    SecurityFunction,
)


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_framework_asset_class_and_frequency_require_names(value: str) -> None:
    with pytest.raises(ValueError, match="name is required"):
        Framework(name=value, version="1.0")

    with pytest.raises(ValueError, match="name is required"):
        AssetClass(name=value)

    with pytest.raises(ValueError, match="name is required"):
        Frequency(name=value)


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_control_requires_core_identifiers_and_description(value: str) -> None:
    with pytest.raises(ValueError, match="domain_id is required"):
        Control(domain_id=value, name="Inventory", number="1.1", description="Desc")

    with pytest.raises(ValueError, match="name is required"):
        Control(domain_id="domain-1", name=value, number="1.1", description="Desc")

    with pytest.raises(ValueError, match="number is required"):
        Control(domain_id="domain-1", name="Inventory", number=value, description="Desc")

    with pytest.raises(ValueError, match="description is required"):
        Control(domain_id="domain-1", name="Inventory", number="1.1", description=value)


def test_grc_models_normalize_trimmed_text_values() -> None:
    framework = Framework(name="  CIS Controls  ", version=" 8.1 ", description="  baseline  ")
    asset_class = AssetClass(name="  Software  ")
    implementation_group = ImplementationGroup(name="  IG1  ", description="  Minimum baseline  ")
    security_function = SecurityFunction(name="  Identify  ", description="  Asset inventory  ")
    frequency = Frequency(name="  Daily  ", description="  Every 24 hours  ")
    domain = Domain(
        framework_id="  CIS-Controls-v8.1  ",
        name="  Inventory and Control of Enterprise Assets  ",
        number=" 1 ",
        description="  Manage enterprise asset inventory.  ",
    )
    control = Control(
        domain_id="  domain-1  ",
        name="  Establish and Maintain a Software Inventory  ",
        number=" 2.1 ",
        description="  Keep software inventory current.  ",
        asset_class_id="  software-class  ",
        implementation_group_id="  ig1  ",
        frequency_id="  daily  ",
    )
    objective = AssessmentObjective(control_id="  control-2-1  ", description="  Validate software inventory quality.  ")
    example = ControlExample(control_id="  control-2-1  ", description="  Endpoint inventory pulls nightly.  ")
    guidance = ControlGuidance(control_id="  control-2-1  ", description="  Include unmanaged software discovery.  ")
    resource = GrcResource(
        title="  CIS Control 2.1 Reference  ",
        url="  https://www.cisecurity.org/controls/inventory-and-control-of-software-assets  ",
    )

    assert framework.name == "CIS Controls"
    assert framework.version == "8.1"
    assert framework.description == "baseline"
    assert asset_class.name == "Software"
    assert implementation_group.name == "IG1"
    assert implementation_group.description == "Minimum baseline"
    assert security_function.name == "Identify"
    assert security_function.description == "Asset inventory"
    assert frequency.name == "Daily"
    assert frequency.description == "Every 24 hours"
    assert domain.framework_id == "CIS-Controls-v8.1"
    assert domain.name == "Inventory and Control of Enterprise Assets"
    assert domain.number == "1"
    assert domain.description == "Manage enterprise asset inventory."
    assert control.domain_id == "domain-1"
    assert control.name == "Establish and Maintain a Software Inventory"
    assert control.number == "2.1"
    assert control.description == "Keep software inventory current."
    assert control.asset_class_id == "software-class"
    assert control.implementation_group_id == "ig1"
    assert control.frequency_id == "daily"
    assert objective.control_id == "control-2-1"
    assert objective.description == "Validate software inventory quality."
    assert example.description == "Endpoint inventory pulls nightly."
    assert guidance.description == "Include unmanaged software discovery."
    assert resource.title == "CIS Control 2.1 Reference"
    assert resource.url == "https://www.cisecurity.org/controls/inventory-and-control-of-software-assets"


def test_control_link_and_related_models_enforce_required_values() -> None:
    with pytest.raises(ValueError, match="control_id is required"):
        ControlLink(
            link_type=ControlLinkType.REQUIRED_CONTROL,
            control_id="",
            required_control_id="control-1",
        )

    with pytest.raises(
        ValueError,
        match="required_control links require required_control_id and disallow resource_id",
    ):
        ControlLink(link_type=ControlLinkType.REQUIRED_CONTROL, control_id="control-2")

    with pytest.raises(
        ValueError,
        match="reference_material links require resource_id and disallow required_control_id",
    ):
        ControlLink(link_type=ControlLinkType.REFERENCE_MATERIAL, control_id="control-2")

    with pytest.raises(ValueError, match="url must be a valid http/https URL"):
        GrcResource(title="Reference", url="ftp://invalid.example")

    with pytest.raises(ValueError, match="description is required"):
        ControlGuidance(control_id="control-2", description="")

    with pytest.raises(ValueError, match="description is required"):
        ControlExample(control_id="control-2", description="\t")


def test_control_link_supports_required_control_and_reference_material_variants() -> None:
    required_link = ControlLink(
        link_type=ControlLinkType.REQUIRED_CONTROL,
        control_id="control-5-1",
        required_control_id="control-6-1",
    )
    reference_link = ControlLink(
        link_type=ControlLinkType.REFERENCE_MATERIAL,
        control_id="control-5-1",
        resource_id="resource-abc",
    )

    assert required_link.required_control_id == "control-6-1"
    assert required_link.resource_id is None
    assert reference_link.resource_id == "resource-abc"
    assert reference_link.required_control_id is None
