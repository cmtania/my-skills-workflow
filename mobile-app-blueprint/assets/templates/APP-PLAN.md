# {{APP_NAME}} app plan

- Status: **{{STATUS}}**
- Platform: **{{PLATFORM}}**
- Updated: **{{DATE}}**

## Product outcome

Describe the user, their problem, and the observable outcome this app should create in one short paragraph.

## Release scope

### In scope

- Define the smallest complete user journey.
- Identify data, device capability, and account requirements.

### Deferred

- List attractive features that are explicitly outside this release.

### Non-goals

- State what the product must not become or promise.

## Assumptions and open decisions

| Item | Status | Owner or validation |
| --- | --- | --- |
| Product audience and distribution | Open decision | Confirm before release planning |
| Offline and account expectations | Open decision | Confirm before persistence design is finalized |

## Delivery slices

| Slice | User-visible outcome | Engineering proof | Exit condition |
| --- | --- | --- | --- |
| 1. Walking skeleton | The primary screen opens and the core action can be attempted | Navigation, state ownership, persistence seam, representative test | Core path runs with deterministic local data |
| 2. Core loop | The smallest useful journey completes end to end | Domain rules and transactional save behavior are covered | Acceptance cases pass without manual data repair |
| 3. Platform integration | Required device or external capability works with fallback behavior | Permission, denial, unavailable, partial, and cancellation paths are exercised | Simulator/static checks and required device checks are recorded separately |
| 4. Release hardening | The app survives lifecycle, restore, accessibility, and failure cases | Regression tests, migration/restore rehearsal, release configuration | Release checklist has evidence and no unowned blocker |

## Acceptance criteria

- Convert the product outcome into observable user behavior.
- Include failure, empty, denied-permission, offline, and recovery cases that apply.
- Define accessibility and privacy expectations for the primary journey.

## Risks

| Risk | Impact | Mitigation or early probe | Status |
| --- | --- | --- | --- |
| Platform-only behavior cannot be proven on the current host | Late discovery on simulator or device | Schedule a thin native build and physical-device check early | Open |

## Verification notes

Record what informed this plan and what remains unverified. Link to [architecture](ARCHITECTURE.md) and [technology stack](TECH-STACK.md).
