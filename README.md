# Transformer Math

Turns ratio arithmetic. 1150 turns against 60 turns is a 115:6 ratio, so 230 V in gives 12 V out. A 2 A draw on the secondary asks 0.1 A from the primary.

## What it computes

- **The ratio truth** - the simplified turns ratio (1 to 100000 turns a side) and the secondary voltage for a primary voltage (0.01 to 10000 V).
- **The current truth** - what a secondary draw (0.01 to 1000 A) asks from the primary, and the power on both sides under ideal arithmetic.
- **The turns truth** - the whole turns to wind for a target secondary voltage, and what those turns actually give.

## Boundary

Arithmetic only. The turns, voltages and current are the owner's own entries, every transformer treated as ideal. It has not seen any build and does not know the core, the wire, the insulation, heat, losses or regulation, and it gives no verdict that a winding, a transformer or a supply is adequate or safe. Mains voltage can kill. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on whole turns and hundredths, half-up on display; power from the exact ratio).
- `oracle.py` - the Python mirror (Fractions) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/transformermath/
Repo: https://github.com/iLanis-agent/transformermath
