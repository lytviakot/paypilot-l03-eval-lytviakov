import json
import sys
from datetime import date

sys.path.insert(0, "/course")
from app.engines import limits

AS_OF = date(2026, 9, 15)

# CUS-0010 (tier3) transfers this month, in EUR (seed: 4200 GBP and 26000 GBP)
transfers = [
    {"date": date(2026, 9, 15), "amount_eur": 4914.0},
    {"date": date(2026, 9, 2), "amount_eur": 30420.0},
]
status = limits.status("tier3", AS_OF, transfers)
monthly = round(status.monthly_remaining_eur, 2)

context = {"customer_id": "CUS-0010", "clock": "2026-09-15T10:00:00Z"}

# the bot's text answer: is the monthly number right?
text_case = {
    "id": "LIM-001",
    "input": "I'm CUS-0010. How much of my MONTHLY transfer limit is left?",
    "expected_output": f"EUR {monthly:,.2f}",
    "context": context,
    "additional_metadata": {
        "layer": "generation",
        "oracle": "engine",
        "assertion": "numeric",
        "expected_number": monthly,
        "tolerance": 1.0,
        "source": "complaint",
        "failure_mode": "daily_as_monthly",
        "severity": "high",
        "runs": 1,
        "gate": "daily",
        "note": "C-09: the bot reported the daily remainder as the monthly one",
    },
}

# the tool result: is the field itself right?
tool_case = {
    "id": "LIM-002",
    "input": "I'm CUS-0010. How much of my monthly transfer limit is left?",
    "expected_output": f"check_limits.monthly_remaining_eur = {monthly:.2f}",
    "context": context,
    "additional_metadata": {
        "layer": "action",
        "oracle": "engine",
        "assertion": "tool_result_numeric",
        "tool": "check_limits",
        "field": "monthly_remaining_eur",
        "expected_number": monthly,
        "tolerance": 1.0,
        "source": "engine",
        "failure_mode": "daily_as_monthly",
        "severity": "critical",
        "runs": 1,
        "gate": "daily",
        "note": "reads the tool payload, because the bot can recompute the number from other fields",
    },
}

for case in (text_case, tool_case):
    print(json.dumps(case, ensure_ascii=False))
