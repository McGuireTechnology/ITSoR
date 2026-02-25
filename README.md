# ITSoR
IT System of Record

## ACL Permissions Model

Domain entities based on `BaseModel` (`Tenant`, `Group`) include:

- `name`: display name
- `owner_id`: owning user id
- `group_id`: owning group id
- `permissions`: a single byte (`0-255`)

`User` is intentionally excluded from `owner_id` and `permissions`.

User model fields:

- `id`
- `name`
- `group_id`
- `email`
- `username`
- `password_hash`

### Permissions Byte Layout

`permissions` is encoded as:

- Bits `7-6`: owner permissions
- Bits `5-4`: group permissions
- Bits `3-2`: world permissions
- Bits `1-0`: control flags

Permission levels are two-bit values:

- `00` = `NONE`
- `01` = `READ`
- `10` = `WRITE`
- `11` = `READ_WRITE`

Control flags (final two bits):

- Bit `1` (`0b10`): `INHERIT_PERMISSIONS`
- Bit `0` (`0b01`): `ACL_LOCKED`

Default permissions are:

- Owner: `READ_WRITE`
- Group: `READ_WRITE`
- World: `NONE`
- Control flags: `0`

Equivalent default byte: `0b11110000` (`240`).

See also: [backend ACL details](backend/README.md#acl-permissions-model).
