# Anomaly severity

Severity is assigned by the deterministic rule engine and must be preserved by the Agent.

| Level | Meaning |
|---|---|
| `INFO` | Informational condition that does not require immediate intervention. |
| `WARNING` | Confirmed anomaly that should be reviewed during normal operations. |
| `CRITICAL` | Confirmed anomaly meeting the rule engine's urgent threshold. |

The Agent may explain why the rule engine returned a level, but must not change it based on narrative judgment.

