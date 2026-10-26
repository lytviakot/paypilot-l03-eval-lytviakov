# What the set does not catch

| Not covered | What happens if it breaks | Decision | Why we live with it |
|---|---|---|---|
| Retrieval over documents (C-13, C-14) | A green run says nothing about retrieved data | Deferred to L04 | The retrieval layer is empty in this set; the cases are written in L04 |
| Memory in a long conversation (C-18) | The bot loses an amount mid-chat and the set stays silent | Deferred to L05 | There are no multi-turn cases yet |
| Tool call parameters | Correct text, wrong tool call | Deferred to L07 | We check tool results, not arguments; the Tool Call Assertion Suite comes in L07 |
| Length and tone of answers (C-17) | A prompt like "be concise" or a cold tone passes unnoticed | Deferred to L09 | Needs an LLM judge, which has to be calibrated first; HUM-005 and HUM-006 are written but need `JUDGE_MODEL` |
| Failure frequency | One run can miss a regression (FX-001 survived the rounding prompt) | Deferred to L08 | Needs `runs: 5` and a statistical assertion |
| Exact window boundary (day 60 vs day 61) | A one-day error at the edge goes unseen | Accepted | The seed only has transactions 57, 63 and 14 days old; moving the clock is not supported by the runner |
| Other languages | An answer in another language is not checked | Accepted | Verta works on one market for now |
