# Identity Workspace

The Identity workspace is where identity inventory and relationship data is managed.

- People - root identity subjects.
- Identities - source-linked identity records for people.
- Users - account principals linked to people.
- Groups - identity groups used for membership modeling.
- Group Memberships - polymorphic membership links (user or group members).

## Client-side URL Convention

The UI uses the route pattern:

`/$workspace/$namespace`

For Identity, the workspace segment is `idm`.

## Identity Routes

- People list: `/idm/people`
- Identities list: `/idm/identities`
- Users list: `/idm/users`
- Groups list: `/idm/groups`
- Group memberships list: `/idm/group-memberships`

Legacy Identity paths (for example `/idm_people`) currently redirect to canonical Identity routes.
