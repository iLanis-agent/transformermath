// Transformer Math engine: turns ratio to secondary voltage, ideal current swap, and the turns to wind for a target voltage. Exact integers (whole turns, hundredths of a V or A), half-up on display.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pi(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,6}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _NP = "the primary turns must be a whole number from 1 to 100000";
var _NS = "the secondary turns must be a whole number from 1 to 100000";
var _V = "the voltage must be from 0.01 to 10000 V with at most two decimal places";
var _A = "the current must be from 0.01 to 1000 A with at most two decimal places";
var _TV = "the target voltage must be from 0.01 to 10000 V with at most two decimal places";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _v(v) { return _dec(v, 2) + " V"; }
function _a(v) { return _dec(v, 2) + " A"; }
function _w(v100, a100) { return _dec(_hu(v100 * a100, 100), 2) + " W"; }
function _gcd(x, y) { while (y) { var t = x % y; x = y; y = t; } return x; }
function _turns(n) { return n + (n === 1 ? " turn" : " turns"); }
function _in(np, ns, vp) {
  return { np: _pi(np, _NP, 1, 100000), ns: _pi(ns, _NS, 1, 100000), vp: _p(vp, _V, 5, 2, 1, 1000000) };
}

function ratioTruth(np, ns, vp) {
  var p = _in(np, ns, vp), g = _gcd(p.np, p.ns);
  var vs = _hu(p.vp * p.ns, p.np);
  var s = "With " + _turns(p.np) + " on the primary and " + _turns(p.ns) + " on the secondary, the ratio is " + (p.np / g) + ":" + (p.ns / g) + ". ";
  return s + _v(p.vp) + " in gives " + _v(vs) + " out.";
}
function currentTruth(np, ns, vp, is_) {
  var p = _in(np, ns, vp), is2 = _p(is_, _A, 4, 2, 1, 100000);
  var vs = _hu(p.vp * p.ns, p.np), ip = _hu(is2 * p.ns, p.np);
  var wIn = _hu(p.vp * is2 * p.ns, 100 * p.np); // exact ratio, not the rounded current
  var s = "A " + _a(is2) + " draw on the " + _v(vs) + " secondary asks " + _a(ip) + " from the " + _v(p.vp) + " primary. ";
  return s + "That is " + _w(vs, is2) + " out and " + _dec(wIn, 2) + " W in.";
}
function turnsTruth(np, vp, target) {
  var npv = _pi(np, _NP, 1, 100000), pv = _p(vp, _V, 5, 2, 1, 1000000), tv = _p(target, _TV, 5, 2, 1, 1000000);
  var nsNeed = _hu(npv * tv, pv); // whole turns, half up
  if (nsNeed < 1) nsNeed = 1;
  var actual = _hu(pv * nsNeed, npv);
  var s = "For " + _v(tv) + " out from " + _v(pv) + " in with " + _turns(npv) + " on the primary, wind " + _turns(nsNeed) + ". ";
  if (actual === tv) return s + "That lands exactly on " + _v(tv) + ".";
  var d = actual - tv, side = d > 0 ? "high" : "low";
  return s + "That actually gives " + _v(actual) + ", " + _v(d > 0 ? d : -d) + " " + side + ".";
}
