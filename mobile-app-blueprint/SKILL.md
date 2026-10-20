---
name: mobile-app-blueprint
description: Create or update a mobile app's APP-PLAN.md, ARCHITECTURE.md, and TECH-STACK.md before implementation or when an existing app needs an accurate technical blueprint. Use for mobile-app planning and architecture documentation; do not use for ordinary feature notes or implementation-only requests.
---

# Mobile App Blueprint

Produce a small, consistent documentation set that another developer or agent can use to build and verify the app without rediscovering its core decisions.

## Choose the mode

- **Greenfield:** Treat architecture and technology choices as proposals. Infer sensible defaults from the requested product and platform, and expose only decisions that materially affect scope, cost, privacy, or delivery.
- **Existing app:** Inspect the repository before writing. Treat manifests, project files, app entry points, state owners, persistence code, native capabilities, and tests as evidence. Clearly separate the current implementation from recommended changes.

Do not stop for routine details that can be recorded as assumptions. Ask only when a missing product or platform choice would produce a materially different system.

For a native iPhone app using SwiftUI, read [references/ios-reference-architecture.md](references/ios-reference-architecture.md). Apply its patterns selectively; product rules and explicit user choices take priority.

## Create the document set

Write these files under `docs/` unless the repository already has a documented convention:

- `APP-PLAN.md` — product outcome, scope, assumptions, delivery slices, acceptance criteria, risks, and unresolved decisions.
- `ARCHITECTURE.md` — system boundaries, source layout, state ownership, data flow, persistence, integrations, concurrency, failure behavior, privacy, accessibility, and test seams.
- `TECH-STACK.md` — platform and deployment targets, languages, frameworks, storage, services, tooling, tests, version policy, and the rationale for each material choice.

Use `scripts/create_docs.py` to create non-destructive scaffolds when Python 3 is available:

```sh
python3 <skill-directory>/scripts/create_docs.py --app-name "App Name" --platform "iOS 17+" --output docs
```

On Windows, `py` can replace `python3`. The script refuses to overwrite existing files unless `--force` is passed. Do not use `--force` unless overwriting those exact documents is part of the user's request. If Python is unavailable, adapt the files in `assets/templates/` manually.

After scaffolding, replace every generic sentence with app-specific content or an explicit `Open decision` entry. A scaffold alone is not a completed result. Follow [references/document-quality.md](references/document-quality.md) while tailoring and reviewing the documents.

## Evidence pass for an existing repository

Inspect only what is needed to make the documents truthful:

1. Read repository instructions and existing product or architecture documentation.
2. Identify the canonical application target and distinguish it from prototypes, migrations, generated outputs, and archived implementations.
3. Inspect package/project manifests, deployment settings, entitlements or permissions, entry points, top-level source folders, persistence, external integrations, and tests.
4. Derive runtime data flow and failure behavior from code, not folder names alone.
5. Record verification limits such as unavailable SDKs, simulators, devices, credentials, or platform services.

Link important claims to repository-relative source paths. Do not present historical or prototype dependencies as part of the production stack.

## Architecture expectations

- Keep product rules in deterministic domain models rather than views or platform adapters.
- Give mutable application state one clear owner and document how features observe or change it.
- Put platform APIs, persistence, networking, notifications, purchases, sensors, and health data behind narrow service boundaries when substitution or testing benefits.
- Define transactional boundaries: say what must be saved together, what is published only after success, and what happens after load/save failures.
- Describe cancellation and stale-result handling for asynchronous work that can outlive navigation, account, restore, or mode changes.
- Keep preview/demo/review data isolated from production data.
- Minimize permissions and collected data; state offline behavior, backup behavior, retention, and user-control expectations.
- Make accessibility, localization, and platform lifecycle behavior part of the architecture rather than a final polish phase.
- Prefer a thin vertical slice and early risk probes over building every layer in isolation.

These are decision criteria, not permission to replace a user-selected architecture.

## Completion check

Before handing off:

- The three documents agree on platform, minimum version, state owner, persistence, integrations, and test strategy.
- Proposed, confirmed, and deferred items are visibly distinguishable.
- Each delivery phase has an observable exit condition.
- Risks name a mitigation or validation task.
- Mermaid diagrams, links, and repository-relative paths are valid where used.
- No claimed build, test, simulator, device, security, or accessibility result exceeds what was actually verified.

Creating these documents does not authorize app implementation, dependency installation, account changes, deployment, or publishing unless the user separately asks for those actions.
