# Residual risk analysis: Golden dataset L03

Set: `golden.jsonl`, `set_hash b7527feb2738`. Mandate: Ship it (L02).

## 1. Coverage matrix

| Layer | Corpus / RAG | Rule engines | Memory | Tools |
| --- | --- | --- | --- | --- |
| Retrieval | not covered | | | not covered |
| Generation | CMP-004, CMP-006 | FX-002..009 (+ `-S`), CMP-003, LIM-001, LIM-005, DIS-001, DIS-002-N, DIS-008, DIS-009, DIS-010, CMP-010, SEC-002, SEC-003, SEM-001, TON-001 | not covered | not covered |
| Action | | LIM-003, DIS-006, DIS-007 | not covered | not covered |

## 2. What the set does not catch

| Not covered | What happens if it breaks | Defer or accept | Why we live with it now |
| --- | --- | --- | --- |
| Retrieval over documents (C-13, C-14) | The bot quotes a wrong table or half an answer and every run stays green | Defer to L04 | The retrieval layer is empty; the cases need the corpus and a reference, which L04 adds |
| Memory in a long conversation (C-18) | The bot forgets an amount mid-chat; the set has no multi-turn cases | Defer to L05 | Multi-turn cases need the dialog runner from L05 |
| Tool call parameters | Right text, wrong account or amount in the tool call | Defer to L07 | We read tool results, not arguments; L07 brings the Tool Call Assertion Suite |
| Tone and length (C-17) | A cold or over-short reply passes every numeric check; only TON-001 looks at tone, and the judge is not configured | Defer to L09 | A judge has to be calibrated first; TON-001 is `gate: release` and needs `JUDGE_MODEL` |
| Number format (decimal comma, thousands separators) | The parser drops commas, so `1086,96` is read as `108696`: a formatting change looks like a wrong amount, and a `not_contains "0.9%"` check passes when the bot writes `0,9%` | Defer to L12 | Fixing it needs a locale-aware parser, which fits when the assertions become a component in L12 |
| Transfer fees (C-01) | The bot states a wrong SWIFT or SEPA fee and no case notices | Defer to the next revision of the set | `fx.transfer_fee` is an engine and the case is cheap to add; it was left out to keep the set within the size target |
| Other languages | An answer in another language is not checked | Accept | Verta works on one market for now |

Complaints outside the set:
- C-02: no customer, general question, not reproducible
- C-15: the mobile app freezes, not an agent problem
- C-16: the bot answered correctly, the customer wants a different product
- C-20: a review with no name, date or text, not reproducible
- C-07: no customer or amount; the best guess is CUS-0007 with 2000 EUR, which is already FX-004 (C-08)
- C-04, C-05: covered by the demo cases FX-003 and FX-003-S (CUS-0005)

## 3. Set size

Cost of one run: calls 30 (`daily` cases x `runs` 1; each agent run makes at least two model calls: the tool call and the answer) · tokens 244,169 (sum of the `tokens` column in `results/hw2/1-baseline-clean.json`, about 8,140 per case) · price about USD 0.034 = **about USD 0.03 per daily run**.

Price assumption: the report holds input and output tokens as one number, so the split is taken from the average call measured in L02 (3,000 in / 310 out) at USD 0.1 in / 0.5 out per million tokens: 244,169 x 0.000455 / 3,310 = USD 0.034. If the stand uses a different model, the figure scales with its price.

Formula from section 7 of the Quality Bar Proposal (L02): `cost = calls x average tokens per call x price per token`.

The release gate adds one case (TON-001, `runs: 5`): 5 more agent runs and 5 judge calls, which are not counted above.

Sensitivity: the prompt change (decimal comma) changed the result on 14 of 30 cases (30/30 to 16/30). The seeded defects changed 13 of 30 (30/30 to 17/30). The set is sensitive enough at this size; more cases would mainly repeat the spread cases.

Under the opposite mandate (Zero regulatory risk) the set would change: every money, limit and dispute case (about 20) must pass at 1.0 and block the release, the share of edge cases and `oracle: human` cases goes up (transfer fees, more window days with a moved clock), and the tone cases get a calibrated judge and become blocking. The run cost grows with the judge calls and `runs: 5`.
