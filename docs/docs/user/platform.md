# Platform Workspace

The Platform workspace is where the ITSoR platform will be managed.

Platform Users - those who sign into the ITSoR application.
Platform Groups - used to manage access to resources within the ITSoR platform.
Platform Tenants - highest security boundary, used to isolate resources.

## Client-side URL Convention

The UI now uses the route pattern:

`/$workspace/$namespace`

For Platform, the workspace segment is `platform`.

## Platform Routes

- Users list: `/platform/users`
- User detail: `/platform/users/:id`
- My account: `/platform/users/me`
- Groups list: `/platform/groups`
- Group detail: `/platform/groups/:id`
- Tenants list: `/platform/tenants`
- Tenant detail: `/platform/tenants/:id`

Legacy paths (for example `/users` or `/groups`) currently redirect to the canonical Platform routes.

## See also

- [Identity Workspace](identity.md)
- [Customization Workspace](customization.md)