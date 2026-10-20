# {{APP_NAME}} technology stack

- Status: **{{STATUS}}**
- Platform: **{{PLATFORM}}**
- Updated: **{{DATE}}**

## Selection principles

State the product constraints that drive technology choices: supported devices, offline behavior, team skills, delivery timeline, privacy, performance, and operating cost.

## Runtime stack

| Layer | Technology and version policy | Status | Why it fits | Evidence or validation |
| --- | --- | --- | --- | --- |
| Platform | {{PLATFORM}} | {{STATUS}} | Native capability and distribution target | Confirm deployment configuration |
| Language | Select the platform language | Open decision | Prefer the smallest production runtime | Confirm in project manifests |
| UI | Select the UI framework | Open decision | Match platform behavior and accessibility | Prove the primary screen on target devices |
| State/domain | Name the ownership and rule model | Open decision | Keep mutations explicit and rules testable | Cover a vertical slice |
| Persistence | Select from actual query, migration, backup, and sharing needs | Open decision | Avoid infrastructure beyond product needs | Rehearse save/load/failure/restore |
| Integrations | List only required native or external services | Open decision | Minimize permissions and third parties | Exercise unavailable and denied paths |

## Development and delivery tooling

| Concern | Choice | Purpose | Required environment |
| --- | --- | --- | --- |
| Project/build | Record the canonical project and generator, if any | Reproducible local and CI builds | Name host and SDK requirements |
| Unit tests | Record framework and test targets | Domain and coordination confidence | Name runnable hosts |
| UI/device validation | Record simulator/device strategy | Rendering, lifecycle, permissions, accessibility | Name devices/accounts/services |
| Packaging/release | Record archive, signing, and store path | Traceable release output | Keep signing secrets out of source |

## Dependency policy

- Prefer platform frameworks and standard libraries when they meet the requirement.
- Add a third-party dependency only with a named capability, owner, version/update policy, privacy impact, license review, and removal path.
- Keep prototypes, generators, and developer tools separate from the production runtime list.
- Pin or constrain versions according to the ecosystem and record minimum supported toolchain versions.

## Environments, configuration, and secrets

Describe development/test/production differences, configuration injection, feature flags, service endpoints, signing, and secret storage. Do not put credentials or private keys in the repository or in this document.

## Rejected or deferred alternatives

| Alternative | Status | Reason | Reconsider when |
| --- | --- | --- | --- |
| Add an evaluated option | Deferred | Explain the current tradeoff | State the evidence that would change the choice |

## Verification notes

List inspected manifests and executed commands for an existing app. Separate configuration inspection, static checks, tests, native builds, simulator checks, physical-device checks, and live-service validation. Link to the [app plan](APP-PLAN.md) and [architecture](ARCHITECTURE.md).
