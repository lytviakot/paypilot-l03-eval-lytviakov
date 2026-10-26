# Run results and deltas

Set: `sets/golden_set.jsonl`, 16 cases (14 in the daily gate, 2 judge cases in the release gate), `set_hash 6e988827b261`.
All three runs use the same set hash, so the differences come from the system, not from the set.

## Runs

| # | Run | Profile | Prompt | Result | Report |
|---|---|---|---|---|---|
| 1 | Baseline | `clean` | `base.v1`, unchanged | **14/14**, exit 0 | `1-baseline-clean.json` |
| 2 | Seeded defects | `lesson-03` | `base.v1`, unchanged | **9/14**, exit 1 | `2-defects-lesson-03.json` |
| 3 | Prompt change | `clean` | `base.v1` + one line (below) | **12/14**, exit 1 | `3-prompt-rounding.json` |

Control run after reverting the prompt (`--profile clean --only FX-003`): PASS.

The report records `prompt_version: base.v1` for runs 1 and 3, because the stand takes the version from the file name, not from its content. The line below is the only record of what changed.

Line appended to `prompts/base.v1.md` for run 3 (then removed with `docker compose up -d --force-recreate stand`):

```
Round all amounts to whole numbers for readability.
```

## Delta 1: baseline to `lesson-03` (14 to 9)

| Case | What failed | Defect |
|---|---|---|
| FX-002 | expected 1078.25, the answer carried 1088.03 | D21 (spread on part of the amount) |
| FX-003 | expected 2154.35, the number did not match | D20 / D21 (wrong tier, spread on part of the amount) |
| DSP-002 | `check_dispute_eligibility.eligible = True`, expected False | D19 (wrong window) |
| DSP-004 | `eligible = True`, expected False | D26 (compliance hold ignored) |
| LIM-002 | `check_limits.monthly_remaining_eur = 95086.0`, expected 964666.0 | D22 (daily remainder shown as monthly) |

All five active defects (D19, D20, D21, D22, D26) turn at least one case red.
LIM-001 (the text answer) still passes on `lesson-03`: the bot recomputes the remainder from other fields. LIM-002 reads the tool payload and catches it.

## Delta 2: baseline to the prompt change (14 to 12)

| Case | What failed |
|---|---|
| FX-001 | expected 1086.96, the answer was rounded |
| FX-002 | expected 1078.25, the answer said 1078 |

The rounding instruction cut the cents, and the tolerance of 0.02 no longer accepted the figure.
Dispute, limit and human cases did not move: the instruction does not touch them.

## Caveat: one run is not a frequency

Two runs of the rounding prompt on the earlier 12-case set and this 16-case set failed different FX cases (FX-002 and FX-003 before, FX-001 and FX-002 now). The model follows the instruction only some of the time. This set proves that the regression is visible; it does not measure how often it happens. That needs `runs: 5` (ladder level 6), listed as deferred in `gaps.md`.
