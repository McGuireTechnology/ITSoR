# Blade Architecture

Blade architecture is a modular, pane-based user experience pattern used in Microsoft-style admin consoles.  
Instead of navigating to a completely new page for every task, the UI opens a new **blade** (a vertical panel) for each level of detail. This keeps context visible, supports progressive drill-down, and reduces navigation loss while performing complex operational tasks.

---

## Why Blade Architecture Exists

Admin workflows are often deep and stateful:

- Start from a broad list (users, devices, policies, subscriptions)
- Open a specific item
- Inspect configuration, health, permissions, logs, and child resources
- Perform changes and validate outcomes

Traditional page-to-page navigation can break user context and force repeated back/forward transitions. Blade architecture addresses this by preserving prior context in a visible stack.

---

## High-Level Structure

The portal is made of a shell plus feature extensions. Each extension contributes blades and actions.

```text
+-----------------------------------------------------------------------------------+
|                                   Portal Shell                                   |
|  Global Nav | Search | Notifications | Tenant Context | Account | Global Actions |
+-------------------------------------+---------------------------------------------+
				      |
			Registers blades, routes, commands
				      |
	      +-----------------------+-----------------------+
	      |                                               |
      +-------------------+                         +-------------------+
      | Extension A       |                         | Extension B       |
      | (e.g., Users)     |                         | (e.g., Policies)  |
      +-------------------+                         +-------------------+
	      |                                               |
	      v                                               v
      +-------------------+                         +-------------------+
      | User List Blade   | ---> opens child --->   | Policy List Blade |
      +-------------------+                         +-------------------+
```

---

## Core Components (Expanded)

## 1) Portal Shell

The shell is the global host of the experience. It owns top-level concerns that are shared across all features.

### Responsibilities

- Global navigation and search
- Tenant/subscription/account context switching
- Notification surface and global status
- Theme, accessibility baseline, localization, and keyboard model
- Startup routing and deep-link resolution

### Typical Contents

- Left navigation rail
- Header with search and global actions
- Session-level providers (auth token, context, feature flags)

---

## 2) Extension (Feature Module)

An extension is a deployable feature unit owned by a product team. It contributes specific blades and commands into the shell.

### Responsibilities

- Registers routes and blade metadata
- Defines command handlers and permissions
- Supplies domain-specific data providers and UI parts
- Encapsulates feature behavior for independent evolution

### Benefits

- Team autonomy and modular ownership
- Safer rollouts using feature flags
- Cleaner separation of domain areas

---

## 3) Blade

A blade is the primary interactive surface for one scope of work. Examples: list, details, create/edit, diagnostics.

### Characteristics

- Opens in a rightward stack
- Receives context from parent blade (resource ID, filters, scope)
- Has its own lifecycle: initialize, load, render, update, dispose
- Can launch additional child blades

### Common Blade Types

- **List Blade**: table/grid of entities and quick actions
- **Details Blade**: summary, properties, related resources
- **Edit/Create Blade**: forms, validation, save/cancel workflow
- **Diagnostics Blade**: health metrics, logs, troubleshooting tasks

---

## 4) Parts / Controls

Parts are reusable building blocks within a blade.

### Examples

- Data grid
- Form section with validation
- Metrics card and sparkline chart
- Tabs/pivots for grouped details
- Inline banners and error summaries

### Responsibilities

- Present focused information cleanly
- Keep interaction patterns consistent across blades
- Enable composition without rewriting full blade layouts

---

## 5) Command Bar

The command bar contains context-sensitive actions for the active blade.

### Typical Actions

- Create / Add
- Edit
- Delete
- Refresh
- Save / Cancel
- Export / Download

### Design Principle

Only show commands valid for current state, role, and selection.

---

## 6) Navigation Context

Navigation context is the payload passed when opening a blade.

### Typical Context Fields

- Tenant/subscription or org scope
- Resource identifiers
- View mode
- Active filters and sort
- Parent-child correlation identifiers

### Why It Matters

- Enables reliable deep linking
- Reconstructs state on refresh/reload
- Preserves parent context while drilling down

---

## 7) Data / Resource Layer

This layer loads and mutates data for blades and parts.

### Responsibilities

- API calls and response normalization
- Loading, empty, partial, and error states
- Retry and timeout handling
- Caching and invalidation
- Optimistic updates when appropriate

### Common Pattern

Blade opens -> fetch required resources -> render partial UI -> hydrate secondary parts.

---

## 8) Policy & Security Layer

Security determines what users can see and do.

### Responsibilities

- RBAC checks for visibility and action permissions
- Tenant and data boundary enforcement
- Conditional rendering for restricted operations
- Audit metadata on critical operations

### UX Impact

Unavailable actions are either hidden or disabled with explanatory messaging.

---

## 9) Telemetry Layer

Telemetry captures behavior and reliability signals across blades.

### Signals Commonly Tracked

- Blade open/close and dwell time
- Command click-through and completion
- API latency and error rates
- Validation failures and save outcomes
- End-to-end funnels (e.g., create policy success)

### Purpose

Improves discoverability, performance, and operational reliability over time.

---

## 10) Lifecycle & State Management

Every blade has a lifecycle and state contract.

### Lifecycle Phases

- Initialize context
- Resolve dependencies
- Load data
- Render interactive UI
- Persist updates
- Dispose subscriptions/resources

### State Concerns

- Unsaved changes guards
- Parent-child refresh orchestration
- Cross-blade event signaling
- Error recovery and retry UX

---

## Blade Stack Illustration

This illustrates context-preserving drill-down from list to details to edit.

```text
Left (older context)                                         Right (active task)

+-------------------+  +-------------------+  +-------------------+
| Users List Blade  |  | User Details      |  | Edit User Blade   |
|-------------------|  |-------------------|  |-------------------|
| Filters, Grid     |  | Profile Summary   |  | Form Fields       |
| Bulk Actions      |  | Groups, Roles     |  | Validation State  |
| Selection Context |  | Child Commands    |  | Save / Cancel     |
+-------------------+  +-------------------+  +-------------------+
	 (still visible)        (still visible)         (current focus)
```

---

## Interaction Flow (ASCII Sequence)

```text
User          Shell           Blade A (List)        Blade B (Details)      Data/API
 |              |                    |                      |                 |
 | Open area    |                    |                      |                 |
 |------------->| route + mount      |                      |                 |
 |              |------------------->| init/load            |                 |
 |              |                    |--------------------->| (none yet)      |
 | Select row   |                    |                      |                 |
 |------------->| open child blade   |                      |                 |
 |              |------------------------------------------>| init            |
 |              |                                           |------fetch----->|
 |              |                                           |<-----data-------|
 |              |                                           | render          |
 | Click Edit   |                                           |                 |
 |------------->| open edit blade                            |                 |
 |              |----------------------------------------------> validate/save |
 |              |                                              |----update----->|
 |              |                                              |<---result------|
 |              |<---------------- notify parent refresh ------|                 |
```

---

## Frontend vs Backend Responsibility Model

This section defines ownership boundaries so blade teams can build quickly without coupling UI concerns to service internals.

### Responsibility Matrix

```text
+------------------------------+-------------------------------+-------------------------------+
| Capability                   | Frontend Responsibility       | Backend Responsibility        |
+------------------------------+-------------------------------+-------------------------------+
| Blade navigation             | Open/close stack, routing     | N/A                           |
| View state                   | Local/UI state, dirty checks  | N/A                           |
| Data retrieval               | Call APIs, map to view model  | Query domain/application data |
| Business rules               | Display-only guardrails       | Source-of-truth enforcement   |
| Validation                   | UX/input validation hints     | Authoritative validation      |
| Authorization                | Hide/disable unavailable ops  | Enforce RBAC/ABAC on request  |
| Multi-tenant scoping         | Send scope/context identifiers| Enforce tenant boundaries     |
| Mutations                    | Submit commands, optimistic UX| Execute use cases + persist   |
| Errors                       | User-friendly messaging/retry | Structured error semantics    |
| Telemetry                    | UX interaction events         | API latency/failure/audit     |
+------------------------------+-------------------------------+-------------------------------+
```

### Frontend Owns

- Blade stack lifecycle (open, focus, close, unsaved-change prompts)
- UX composition (parts, forms, command bar, empty/loading/error states)
- Client-side state orchestration across parent/child blades
- Request correlation and cancellation (debounce/search/abort behavior)
- View-model mapping from transport DTOs to UI-specific shape
- Accessibility, keyboard interactions, and progressive rendering behavior

### Backend Owns

- Domain invariants and business policy enforcement
- Authorization decisions for every read/write operation
- Validation of payload correctness and referential consistency
- Transactional integrity, concurrency handling, and persistence
- Stable API contracts, idempotency behavior, and version strategy
- Audit trail, security controls, and operational observability

---

## Contract Boundary: What Must Never Move to the Frontend

These concerns are always backend-authoritative, even if mirrored in UI for better user guidance:

- Access control decisions (who can do what)
- Cross-tenant isolation and data boundary checks
- Canonical business rules and invariants
- Final validation and conflict detection
- Security-sensitive derivations (effective roles, policy evaluations)

If frontend logic and backend logic disagree, backend decisions win.

---

## Contract Boundary: What Must Stay in the Frontend

These concerns belong in the UI layer for responsiveness and usability:

- Blade presentation and command placement
- Interaction timing and transient state (expanded rows, tab selection, inline draft values)
- Optimistic rendering and local rollback behavior
- Human-readable messaging and remediation guidance

Backend should avoid prescribing UI layout details.

---

## End-to-End Request Ownership (ASCII)

```text
User Action: "Save changes" in Edit Blade

Frontend (Blade)                             Backend (API + Application + Domain)
------------------                           -------------------------------------
1) Collect form data
2) Run UX validation (required fields)
3) Build command payload  ------------------> 4) Authenticate + authorize
4) Attach context headers (tenant, corrId)    5) Validate schema + business rules
5) Disable save / show spinner                6) Execute use case transaction
6) Render optimistic update (optional)        7) Persist + publish domain events
7) Handle response <-----------------------   8) Return result/error contract
8) Reconcile blade state
9) Notify parent blade refresh
```

---

## API Shape Guidance for Blade Teams

Use contracts that support blades directly, while keeping domain models internal.

### Read APIs (for list/details blades)

- Return transport DTOs tailored for UI consumption
- Support pagination/filter/sort server-side for large datasets
- Include minimal metadata needed for command enablement

### Write APIs (for create/edit blades)

- Accept command-style payloads (intent-focused)
- Return deterministic error categories:
	- `validation_error`
	- `authorization_error`
	- `conflict_error`
	- `transient_error`
- Provide correlation identifiers for troubleshooting and telemetry joins

---

## Blade Lifecycle with Responsibility Tags

```text
[FE] Open blade -> [FE] Resolve route/context -> [FE] Request data
		-> [BE] Authorize + query -> [BE] Return DTO
		-> [FE] Render parts + commands
		-> [FE] User edits + local validation
		-> [FE] Submit command
		-> [BE] Validate + enforce policy + persist
		-> [BE] Return outcome
		-> [FE] Reconcile UI + refresh parent blades
```

---

## Implementation Checklist (Developer)

- Frontend checks command visibility from backend-provided capabilities, not hardcoded assumptions
- Backend rejects unauthorized and out-of-scope operations even when UI hides actions
- Frontend treats backend errors as typed outcomes, not string parsing
- Backend guarantees stable response contracts per API version
- Frontend includes correlation IDs in outbound calls and telemetry events
- Both layers emit telemetry that can be joined for one user journey

---

## Practical Advantages

- **Context retention**: users keep prior blades visible while working deeper
- **Operational efficiency**: fewer full-page transitions in administrative workflows
- **Composability**: reusable parts and extension-based ownership
- **Governance**: policy checks and telemetry integrated into each blade interaction

---

## Practical Tradeoffs

- Deep blade stacks can increase cognitive load
- State synchronization between parent/child blades can become complex
- Performance tuning is required to avoid latency in multi-blade workflows
- Overly dense command surfaces can reduce discoverability

---

## Summary

Blade architecture is a task-oriented, context-preserving pattern for complex admin operations.  
Its core strength is combining modular feature ownership (extensions) with progressive, stacked workflows (blades), backed by strong data handling, security policy enforcement, and telemetry.

---

## Glossary

- **Blade**: A vertical panel representing one focused scope of work (list, details, edit, diagnostics).
- **Blade Stack**: The ordered set of open blades, where each new blade opens to the right while prior context remains visible.
- **Portal Shell**: The global host frame that provides navigation, identity/tenant context, notifications, and shared platform services.
- **Extension**: A feature module that registers blades, commands, routes, and domain logic into the shell.
- **Part / Control**: A reusable UI building block inside a blade, such as a grid, form, card, tab set, or chart.
- **Command Bar**: A contextual action surface for the active blade (for example, create, edit, delete, refresh, save).
- **Navigation Context**: Structured data passed between blades (IDs, scope, filters, mode) to preserve state and support deep links.
- **Resource / Data Layer**: Services that load, cache, transform, and persist data for blade experiences.
- **RBAC**: Role-based access control that determines which data and actions are visible or allowed for a user.
- **Telemetry**: Instrumentation events and metrics used to analyze reliability, performance, and user workflows.
- **Lifecycle**: The sequence of blade states from initialization and data load through interaction, save, and disposal.
- **Deep Link**: A URL or route that opens a specific blade with enough context to reconstruct the intended view.
