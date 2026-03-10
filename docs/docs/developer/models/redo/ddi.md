# DDI Domain Models

DDI (DNS, DHCP, IPAM) models define the network source of truth for naming, addressing, and dynamic assignment.

## Why DDI

- IPAM alone answers address planning and allocation.
- DDI adds DNS and DHCP operational truth needed for real service discovery and endpoint lifecycle.
- For ITSoR, DDI is the better slice for control evidence, drift detection, and operational troubleshooting.

## Scope

- DNS zones and records
- DHCP scopes, leases, and reservations
- IP spaces, subnets, addresses, and assignment history
- Name-to-address consistency and ownership traceability

## Core Entities

| Entity | Purpose | Required Fields |
| --- | --- | --- |
| `dns_zone` | Authoritative domain partition | `zone_id`, `fqdn`, `zone_type`, `authority`, `state` |
| `dns_record` | Record in a DNS zone | `dns_record_id`, `zone_id`, `record_type`, `name`, `value`, `ttl`, `state`, `valid_from`, `valid_to` |
| `dhcp_scope` | Address pool for lease issuance | `scope_id`, `subnet_id`, `range_start`, `range_end`, `lease_duration`, `state` |
| `dhcp_lease` | Time-bound dynamic address assignment | `lease_id`, `scope_id`, `ip_id`, `client_id`, `hostname`, `issued_at`, `expires_at`, `state` |
| `dhcp_reservation` | Deterministic host-to-address reservation | `reservation_id`, `scope_id`, `ip_id`, `client_id`, `hostname`, `state` |
| `ip_space` | Top-level address-space boundary | `ip_space_id`, `address_family`, `cidr`, `state`, `owner_ref` |
| `subnet` | Allocatable network segment | `subnet_id`, `ip_space_id`, `cidr`, `site_ref`, `vlan_ref`, `state` |
| `ip_address` | Individual address record | `ip_id`, `subnet_id`, `address`, `allocation_type`, `state`, `assigned_at`, `released_at` |
| `ip_assignment` | Assignment history to assets/interfaces/services | `assignment_id`, `ip_id`, `target_type`, `target_id`, `interface_ref`, `valid_from`, `valid_to` |
| `name_ip_binding` | Authoritative DNS-to-IP linkage | `binding_id`, `dns_record_id`, `ip_id`, `binding_type`, `valid_from`, `valid_to` |

## Relationships

- `dns_zone` contains `dns_record`
- `dhcp_scope` allocates `dhcp_lease`
- `dhcp_scope` maintains `dhcp_reservation`
- `ip_space` contains `subnet`
- `subnet` contains `ip_address`
- `ip_address` is assigned through `ip_assignment`
- `dns_record` maps to `ip_address` through `name_ip_binding`
- `dhcp_lease` references `ip_address`
- `dhcp_reservation` references `ip_address`

## Lifecycle States

### `ip_address.state`

- `available`
- `reserved`
- `assigned`
- `quarantined`
- `released`

### `dns_record.state`

- `active`
- `staged`
- `deprecated`
- `removed`

### `dhcp_lease.state`

- `active`
- `expired`
- `released`
- `conflict`

## Integrity Rules

1. No active duplicate address assignment in the same subnet.
2. DNS `A`/`AAAA` records should resolve to active `ip_address` records through `name_ip_binding`.
3. DHCP leases must fall inside an active scope range.
4. Reservations cannot collide with active dynamic leases unless explicitly overridden.
5. Historical lease and DNS change events are retained for forensic reconstruction.

## Domain Name Tracking Guidance

- DDI tracks domain names through `dns_zone` and `dns_record` entities.
- `name_ip_binding` provides explicit traceability between DNS names and managed IP addresses.
- This supports forward and reverse lookup integrity, stale-record detection, and service ownership tracing.

## Standards Alignment

| Standard | Mapping |
| --- | --- |
| ITIL v4 | Service Configuration Management, Infrastructure and Platform Management |
| CIS Controls v8 | Control 1, Control 12, Control 13 |
| NIST CSF 2.0 | `ID.AM`, `PR.PS`, `DE.CM` |
| ISO/IEC 27001:2022 | Network security operations and asset traceability controls |

## Cross-Slice Dependencies

- DDI targets and assignments resolve to ITAM assets and services.
- Ownership and steward references resolve to IDM principals.
- Misconfiguration, exposure, and drift findings are asserted and evidenced in GRC.
