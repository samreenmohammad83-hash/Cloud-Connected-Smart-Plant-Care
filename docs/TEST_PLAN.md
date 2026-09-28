# Test Plan

| ID | Scenario | Input | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|
| T01 | Simulator starts | Run simulator | Readings generated | Record during demo | — |
| T02 | Valid sensor data | Moisture 55 | 200 accepted | — | — |
| T03 | Invalid moisture | 150 | 422 rejected | — | — |
| T04 | Invalid API key | Wrong key | 401 rejected | — | — |
| T05 | Store reading | Valid payload | DB row created | — | — |
| T06 | Latest reading | GET latest | Latest row returned | — | — |
| T07 | History | GET history | Historical rows returned | — | — |
| T08 | Above threshold | 55% | No auto watering | — | — |
| T09 | Below threshold | 29% | Auto watering eligible | — | — |
| T10 | Watering event | Trigger | Event stored | — | — |
| T11 | Moisture increase | Pump simulation | Simulator raises moisture | — | — |
| T12 | Manual water | POST water | Event returned | — | — |
| T13 | Cooldown | Rapid second trigger | Suppressed | — | — |
| T14 | Alert | Low moisture | Warning stored | — | — |
| T15 | Acknowledge | Alert ID | Status ACKNOWLEDGED | — | — |
| T16 | Offline | Stale last_seen | Offline alert | — | — |
| T17 | Dashboard | Browser | Current cards/charts shown | — | — |
| T18 | Multiple devices | 2+ device IDs | Independent telemetry | — | — |
| T19 | API failure | Stop backend | Simulator logs retry/error | — | — |
| T20 | Database failure | Stop DB | Service returns failure; monitoring required | — | — |
