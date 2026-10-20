# Apple Health daily reward pattern

Use this reference when an iPhone app should reproduce StepForge's daily chest mechanic or adapt it to another reward type. Preserve the behavioral invariants; rename chest, weapon, element, or rarity concepts to fit the new product.

## Product truth

The free daily chest is **calendar-granted, not Health-gated**:

- Grant one free daily slot for every eligible local calendar day, including zero-step days and days for which Health data is unavailable.
- Apple Health activity changes the chest tier and reward odds. It does not decide whether the free daily chest exists.
- A day without a visible step quantity gets the common-only tier. Do not pretend missing Health access is a measured zero in the receipt or UI.
- A personal step goal affects the streak bonus only. It does not block the chest or replace the fixed tier thresholds.

If a new product truly requires Health connection before granting anything, record that as an explicit deviation with permission-denied, unavailable-device, and App Review consequences. Do not silently introduce that gate while claiming StepForge parity.

## Daily lifecycle

Use the user's calendar and time zone rather than fixed 24-hour intervals.

1. Build stable day keys such as `YYYY-MM-DD` from local calendar components.
2. On launch, foreground refresh, and date rollover, reconcile today plus the previous six calendar days.
3. Add the free daily slot to each day exactly once. Store earned slots as data; do not infer them only from the current time.
4. Assign each new slot one uniformly selected element and persist that element before a reward is rolled.
5. Keep an unopened slot recoverable until the seventh local midnight after its day. Today plus the previous six dates therefore remain available.
6. Never mutate persistence merely because the UI rendered a chest card, tier label, or history row.

Optional paid extras follow a separate entitlement rule: grant them only for dates covered by a verified benefit period. Once earned, they remain usable through their normal expiry even if entitlement later lapses. A later purchase must not retroactively mint extras for uncovered dates.

## Health data contract

Request read-only access to:

- step count;
- walking/running distance;
- active energy burned.

Do not request Health write access for this mechanic. Exclude samples marked as manually entered. Query cumulative totals per calendar day and retain an availability flag for every metric because HealthKit does not reveal read-denial status directly.

Treat each metric independently:

- If a returned day has a visible quantity, replace the saved value for that metric.
- If no quantity is visible, retain the last locally saved value rather than erasing it.
- Never estimate distance or energy from steps.
- Never describe a missing value as an authorization decision that HealthKit did not disclose.

StepForge reads 30 days for progression history and presents the latest seven days as the recoverable chest timeline. An adapted product may choose another history window, but reward expiry and the query window must be documented separately.

## Tier and rarity rules

Snapshot the day's steps when the reward draft is first created.

| Steps | Tier | Common | Uncommon | Rare | Epic | Mythic |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 0–2,500 | Common/Wooden | 100% | 0% | 0% | 0% | 0% |
| 2,501–5,000 | Iron | 70% | 30% | 0% | 0% | 0% |
| 5,001–7,500 | Silver | 50% | 32% | 18% | 0% | 0% |
| 7,501–9,999 | Gold | 38% | 30% | 22% | 10% | 0% |
| 10,000+ | Mythic | 30% | 28% | 24% | 13% | 5% |

A qualifying streak is consecutive days with an available step reading at or above that day's saved personal goal. Each streak day moves one percentage point from Common to the highest rarity currently unlocked, capped at 15 points. It never unlocks a rarity above the day's tier.

Example: a 4-day streak at Gold changes `38/30/22/10/0` to `34/30/22/14/0`.

## Reward selection

Keep granting, drafting, and completion as three separate states:

```text
earned slot -> saved unopened draft -> saved completed reward
```

- **Grant:** Save the day, slot kind, and assigned element. Do not choose a rarity or item while rendering the UI.
- **Draft:** On the user's first open attempt, roll rarity from the saved day's tier and streak, then choose an item within the assigned element and rolled rarity. Give unowned eligible items weight `2` and already-owned items weight `1`.
- **Freeze:** Save the complete receipt and selected item before presenting the reveal. Later steps, goal changes, app restarts, or Health refreshes must not reroll it.
- **Complete:** Atomically save the opened timestamp, ownership/copy count, refinement result, and any initial showcase choice. Publish the new visible state only after that save succeeds.

The receipt should include:

- stable opening ID formed from day key and slot kind;
- reward/item ID;
- tier;
- step goal and activity values used for the roll;
- per-metric availability flags;
- creation and completion timestamps or equivalent lifecycle fields.

Catalog eligibility is product-specific. Exclude campaign-only, purchased-only, or otherwise non-loot items before weighted selection.

## Failure and idempotency rules

- Loading failure disables writes so a damaged or unreadable save cannot be replaced by default state.
- Grant, draft, and completion each use a copy-save-publish transaction.
- A failed grant save must not make a slot appear earned.
- A failed draft save must not reveal a reward.
- A failed completion save must leave the chest unopened and ownership unchanged.
- Completing the same opening twice is a no-op; it must not duplicate inventory.
- An expired draft cannot be completed after its slot expires.
- Restoring or migrating an existing receipt must preserve its original reward and activity snapshot.

## Refresh and observer flow

Register Health observers synchronously during app launch after the user has previously requested Health access. Enable background delivery separately. On an observer callback:

```text
observer callback
  -> coalesced Health refresh
  -> query daily totals
  -> merge only available metrics
  -> reconcile calendar slots and entitlements
  -> atomically save progress
  -> update dependent notifications/widgets
  -> acknowledge observer completion
```

Also refresh on initial connection, launch, foreground entry, manual refresh, and relevant observer callbacks. Coalesce concurrent refresh requests, cancel superseded work when appropriate, and reject results that belong to an obsolete profile, restore generation, or preview mode.

Background delivery is system-scheduled; do not promise an exact refresh time. If Health is unavailable, denied, empty, or fails, preserve saved progress and keep the free daily chest usable.

## Isolation, privacy, and presentation

- Keep preview/review activity and rewards in an in-memory store separate from production.
- Store Health-derived progress locally with atomic writes and suitable file protection.
- Decide and document whether the file is excluded from device cloud backups; StepForge excludes it and provides an explicit collection backup flow.
- Explain that Health access is read-only and optional for the free chest, and that more steps improve possibilities rather than guaranteeing a rare reward.
- Show metric availability honestly in reward history. A zero with a visible sample is different from an unavailable value.

## Required verification cases

Cover these behaviors with deterministic tests and injected calendar, clock, store, Health samples, and random source:

- a no-Health, zero-step day still receives exactly one common-only daily chest;
- every threshold boundary maps to the expected tier and maximum rarity;
- odds total 100%, streak bonus caps at 15, and locked rarities remain impossible;
- UI/card rendering performs no write and no reward roll;
- today and the previous six local dates are recoverable, with expiry at the seventh midnight;
- Health backfill updates activity without duplicating slots;
- a missing metric does not erase its previous saved value;
- manually entered Health samples are excluded;
- a saved draft survives reload and cannot be rerolled by later activity;
- completion is idempotent and a save failure grants no item;
- verified paid coverage grants only its eligible extra slots, which remain earned after lapse;
- late refresh results cannot contaminate restored, preview, or different-profile state;
- native Health behavior is separately checked on a physical iPhone.
