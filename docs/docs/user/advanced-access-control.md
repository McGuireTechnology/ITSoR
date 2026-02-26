# User's Guide

## Databases

Databases

Schemas

Entities

Records

Attributes

Values


## Projects / Apps

## Security and Access Control

The API uses OAuth2 password bearer tokens for authenticated access.

### 1) Get an access token

POST /auth/token with form fields:

- username
- password

Example:

curl -X POST http://localhost:8000/auth/token \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=admin&password=admin"

Use the returned access_token as a Bearer token in Authorization headers.

### 2) Manage users, tenants, and groups

Core endpoints:

- Users: /users and /users/{user_id}
- Tenants: /tenants and /tenants/{tenant_id}
- Groups: /groups and /groups/{group_id}

All support List, Create, Read, Replace, Update, Delete.

### 3) Record permissions (CRUD)

Record ACL fields are stored under acl:

- owner_user_id
- owner_perms (for example: ["create", "read", "update", "delete"])
- group_perms (map of group_id to permission lists)
- tenant_perms (map of tenant_id to permission lists)
- public_perms (permission list for all authenticated users)

To create, read, update, or delete a record, a user must have the needed permission by one of:

- Owner match
- Group membership
- Tenant membership
- Public permissions

Required permission by operation:

- POST /records: create (applied by ACL definition during record creation)
- GET /records and GET /records/{record_id}: read
- PUT/PATCH /records/{record_id}: update
- DELETE /records/{record_id}: delete

### 4) Create a record with ACL

Example:

curl -X POST http://localhost:8000/records \
	-H "Authorization: Bearer <access_token>" \
	-H "Content-Type: application/json" \
	-d '{
		"entity_id": "entity-1",
		"data": {"name": "Sample Record"},
		"acl": {
			"owner_perms": ["create", "read", "update", "delete"],
			"group_perms": {"group-admins": ["read", "update"]},
			"tenant_perms": {"tenant-default": ["read"]},
			"public_perms": []
		}
	}'

### 5) Quick flow

1. Authenticate and get token.
2. Create tenant and group.
3. Create user and attach them to tenant/group.
4. Create record ACL entries for owner/group/tenant/public.
5. Validate access using GET, PATCH, and DELETE with different users.