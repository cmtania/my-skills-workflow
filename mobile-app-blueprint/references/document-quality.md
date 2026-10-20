# Blueprint document quality

Apply these rules to all three generated documents.

## Status language

Use consistent labels:

- **Confirmed** — supported by source, configuration, a user decision, or an executed check.
- **Proposed** — the recommended choice for a greenfield app or future change.
- **Deferred** — intentionally outside the current release or phase.
- **Open decision** — a choice that needs product or engineering input before implementation.

Never turn an assumption into a confirmed fact. State when a document describes the target architecture rather than the current repository.

## Cross-document contract

`APP-PLAN.md` owns product scope and delivery order. `ARCHITECTURE.md` owns boundaries and runtime behavior. `TECH-STACK.md` owns concrete technologies and version policy. Link between the documents instead of copying long sections.

Keep these facts identical everywhere they appear:

- canonical app target and supported platforms;
- minimum operating-system version;
- application state owner;
- persistence mechanism and migration policy;
- native/external integrations and permissions;
- test layers and known verification limits.

## Useful specificity

Prefer statements that constrain implementation and testing:

- Weak: "Use clean architecture."
- Useful: "Views send intents to the main-actor app model; deterministic domain models do not import SwiftUI; file and HealthKit effects enter through service protocols."
- Weak: "Handle errors."
- Useful: "Publish a hatch result only after the outcome and inventory consumption are atomically persisted; on save failure, retain the prior visible state and show a recoverable error."

Name the owner, trigger, data, boundary, failure behavior, and verification method for important flows.

## Diagrams

Use a Mermaid diagram only when it clarifies at least three components or a non-trivial sequence. Keep node labels short and accompany the diagram with prose that states the important invariant. Do not use a diagram as decoration.

## Verification record

End each document with either evidence/verification notes or links to a shared verification section. Distinguish:

- source/configuration inspection;
- static checks;
- unit/integration tests;
- native compilation;
- simulator rendering;
- physical-device behavior;
- live service or account validation.

If a layer was unavailable, say so directly and add the next validation action to the plan.
