import json
import sys
from datetime import date

sys.path.insert(0, "/course")
from app.engines import disputes

AS_OF = date(2026, 9, 15)   # "today" for the whole run

# (id, customer, transaction, transaction date, reason, compliance hold)
transactions = [
    ("DSP-001", "CUS-0004", "TX-0401", date(2026, 7, 20), "duplicate_charge", False),    # 57 days old, window is 60
    ("DSP-002", "CUS-0004", "TX-0402", date(2026, 7, 14), "duplicate_charge", False),    # 63 days old, past the window
    ("DSP-003", "CUS-0004", "TX-0403", date(2026, 9, 1), "duplicate_charge", False),     # 14 days old, middle of the range
    ("DSP-004", "CUS-0006", "TX-0601", date(2026, 8, 16), "goods_not_received", True),   # the hold blocks it
]

for cid, cust, tx, tx_date, reason, hold in transactions:
    result = disputes.check(reason, tx_date, "settled", AS_OF, hold)
    days_old = (AS_OF - tx_date).days
    case = {
        "id": cid,
        "input": f"Check whether transaction {tx} can be disputed under {reason.replace('_', ' ')}.",
        "expected_output": f"check_dispute_eligibility.eligible = {str(result.eligible).lower()}",
        "context": {
            "customer_id": cust,
            "transaction_id": tx,
            "reason_code": reason,
            "clock": "2026-09-15T10:00:00Z",
        },
        "additional_metadata": {
            "layer": "action",
            "oracle": "engine",
            "assertion": "tool_result_flag",
            "tool": "check_dispute_eligibility",
            "field": "eligible",
            "expected_flag": result.eligible,
            "source": "engine",
            "failure_mode": "engine_seam" if hold else "wrong_window",
            "severity": "critical",
            "runs": 1,
            "gate": "daily",
            "note": f"{days_old} days since the transaction, window is {result.window_days}",
        },
    }
    print(json.dumps(case, ensure_ascii=False))
