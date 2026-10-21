# Transformer Math oracle: independent Fraction mirror of engine.js. Writes expected.json.
import json
from math import gcd
from fractions import Fraction

NP = "the primary turns must be a whole number from 1 to 100000"
NS = "the secondary turns must be a whole number from 1 to 100000"
V = "the voltage must be from 0.01 to 10000 V with at most two decimal places"
A = "the current must be from 0.01 to 1000 A with at most two decimal places"
TV = "the target voltage must be from 0.01 to 10000 V with at most two decimal places"

def pi(t, err, lo, hi):
    t = t.strip()
    if not t.isdigit() or len(t) > 6:
        raise ValueError(err)
    v = int(t)
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def p(t, err, lo, hi):
    t = t.strip()
    parts = t.split(".")
    if len(parts) > 2 or not parts[0].isdigit() or (len(parts) == 2 and (not parts[1].isdigit() or len(parts[1]) > 2)):
        raise ValueError(err)
    v = int(parts[0]) * 100 + int(parts[1].ljust(2, "0")) if len(parts) == 2 else int(parts[0]) * 100
    if v < lo or v > hi:
        raise ValueError(err)
    return v

def hu(n, d):
    return (2 * n + d) // (2 * d)

def dec(v):
    s, f = str(v // 100), str(v % 100).rjust(2, "0").rstrip("0")
    return s + "." + f if f else s

def vv(x): return dec(x) + " V"
def aa(x): return dec(x) + " A"
def ww(v100, a100): return dec(int(hu(Fraction(v100) * a100, 100))) + " W"
def turns(n): return str(n) + (" turn" if n == 1 else " turns")

def inn(np_, ns_, vp_):
    return pi(np_, NP, 1, 100000), pi(ns_, NS, 1, 100000), p(vp_, V, 1, 1000000)

def ratioTruth(np_, ns_, vp_):
    npx, nsx, vp = inn(np_, ns_, vp_)
    g = gcd(npx, nsx)
    vs = int(hu(Fraction(vp) * nsx, npx))
    return "With " + turns(npx) + " on the primary and " + turns(nsx) + " on the secondary, the ratio is " + str(npx // g) + ":" + str(nsx // g) + ". " + vv(vp) + " in gives " + vv(vs) + " out."

def currentTruth(np_, ns_, vp_, is_):
    npx, nsx, vp = inn(np_, ns_, vp_)
    is2 = p(is_, A, 1, 100000)
    vs = int(hu(Fraction(vp) * nsx, npx))
    ip = int(hu(Fraction(is2) * nsx, npx))
    win = int(hu(Fraction(vp) * is2 * nsx, 100 * npx))
    return "A " + aa(is2) + " draw on the " + vv(vs) + " secondary asks " + aa(ip) + " from the " + vv(vp) + " primary. That is " + ww(vs, is2) + " out and " + dec(win) + " W in."

def turnsTruth(np_, vp_, target):
    npx = pi(np_, NP, 1, 100000); pv = p(vp_, V, 1, 1000000); tv = p(target, TV, 1, 1000000)
    nsn = int(hu(Fraction(npx) * tv, pv))
    if nsn < 1: nsn = 1
    actual = int(hu(Fraction(pv) * nsn, npx))
    s = "For " + vv(tv) + " out from " + vv(pv) + " in with " + turns(npx) + " on the primary, wind " + turns(nsn) + ". "
    if actual == tv:
        return s + "That lands exactly on " + vv(tv) + "."
    d = actual - tv
    return s + "That actually gives " + vv(actual) + ", " + vv(d if d > 0 else -d) + " " + ("high" if d > 0 else "low") + "."

FNS = {"ratioTruth": ratioTruth, "currentTruth": currentTruth, "turnsTruth": turnsTruth}

cases = []
nps = ["1", "10", "1150", "99999", "100000"]
nss = ["1", "60", "1150", "7777", "100000"]
vps = ["0.01", "5", "12", "230", "10000"]
for np_ in nps:
    for ns_ in nss:
        for vp_ in vps:
            cases.append(("ratioTruth", [np_, ns_, vp_]))
for a in ["0.01", "0.5", "2", "1.37", "999.99", "1000"]:
    cases.append(("currentTruth", ["1150", "60", "230", a]))
    cases.append(("currentTruth", ["1", "100000", "0.01", a]))
for t in ["0.01", "6.3", "12", "230", "10000"]:
    cases.append(("turnsTruth", ["1150", "230", t]))
    cases.append(("turnsTruth", ["1", "0.01", t]))
    cases.append(("turnsTruth", ["100000", "10000", t]))
errs = ["0", "100001", "1.5", "x", ""]
out = []
for name, args in cases:
    fn = FNS[name]
    try: exp = fn(*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": name, "args": args, "expected": exp})
for bad in errs:
    for name, args in [("ratioTruth", [bad, "60", "230"]), ("ratioTruth", ["1150", bad, "230"]),
                       ("ratioTruth", ["1150", "60", bad]), ("currentTruth", ["1150", "60", "230", bad]),
                       ("turnsTruth", ["1150", "230", bad]), ("turnsTruth", [bad, "230", "12"]),
                       ("turnsTruth", ["1150", bad, "12"])]:
        fn = FNS[name]
        try: exp = fn(*args)
        except ValueError as e: exp = "ERR:" + str(e)
        out.append({"fn": name, "args": args, "expected": exp})
with open("expected.json", "w") as fh:
    json.dump(out, fh, indent=1)
print(len(out), "cases written")
