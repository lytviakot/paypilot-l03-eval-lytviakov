import json
import sys

sys.path.insert(0, "/course")
from app.engines import fx

amounts = [1000, 1001, 2000]   # three amounts for CUS-0007

for i, amount in enumerate(amounts, start=1):
    q = fx.quote(amount, "EUR", "USD", "tier2", allowance_used_eur=0.0)
    case = {
        "id": f"FX-{i:03d}",
        "input": f"I'm CUS-0007. Convert {amount} EUR to USD. What is the final amount I receive?",
        "expected_output": f"{q.final_amount:.2f} USD",
        "context": {"customer_id": "CUS-0007", "clock": "2026-09-15T10:00:00Z"},
        "additional_metadata": {
            "layer": "generation",
            "oracle": "engine",
            "assertion": "numeric",
            "expected_number": round(q.final_amount, 2),
            "tolerance": 0.02,
            "source": "engine",
            "failure_mode": "wrong_spread",
            "severity": "high",
            "runs": 1,
            "gate": "daily",
        },
    }
    print(json.dumps(case, ensure_ascii=False))
