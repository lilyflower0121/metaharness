# Skill Gate Readiness Checklist

Use before accepting a metaharness skill as gate-ready.

- [ ] The skill has a risk tier or meta role.
- [ ] The skill names an exact gate command.
- [ ] Required contract fields are documented.
- [ ] A valid fixture passes the gate.
- [ ] An invalid fixture fails the gate.
- [ ] High-risk skills require authority and rollback/irreversibility.
- [ ] The validator fails closed on missing fields.
- [ ] Phase-sensitive flows declare a lifecycle phase and pass `phase_risk_gate.py`.
- [ ] MVP/exploration gates are lighter than merge/release gates unless high-risk escalators are present.
- [ ] The validator does not print secret values.
