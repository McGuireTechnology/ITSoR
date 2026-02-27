# Customization Workspace

The Customization workspace is where model-driven SoR structure is configured.

- Workspaces - top-level customization boundaries.
- Namespaces - organizational slices within workspaces.
- Entity Types - schema-like definitions for records.
- Entity Records - data instances stored under entity types.

## Client-side URL Convention

The UI uses the route pattern:

`/$workspace/$namespace`

For Customization, the workspace segment is `customization`.

## Customization Routes

- Workspaces list: `/customization/workspaces`
- Workspace detail: `/customization/workspaces/:id`
- Namespaces list: `/customization/namespaces`
- Namespace detail: `/customization/namespaces/:id`
- Entity types list: `/customization/entity-types`
- Entity type detail: `/customization/entity-types/:id`
- Entity records list: `/customization/entity-records`
- Entity record detail: `/customization/entity-records/:id`

Legacy Customization paths (for example `/workspaces` or `/entity-types`) currently redirect to canonical Customization routes.
