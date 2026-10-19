const c = require('./calc.js'), a = require('assert');
a(Math.abs(c.rer(10) - 393.6) < 0.5);
a(Math.abs(c.mer(10, 'neutered') - 629.8) < 1);
a.equal(c.fmtCups(2.25), '2 1/4'); a.equal(c.fmtCups(0.06), '0'); a.equal(c.fmtCups(0.5), '1/2');
const s = c.switchCups(2, 500, 378); a(Math.abs(s.cups - 2.6455) < 0.001); a(s.change < 0);
const p = c.mixPlan(800, 400, 350); a(Math.abs(p[2].newCups * 350 + p[2].oldCups * 400 - 800) < 1e-9);
const f = c.portions(630, { kcal_cup: 420, kcal_kg: 3800 }); a(Math.abs(f.cups - 1.5) < 1e-9); a(Math.abs(f.grams - 165.8) < 0.1);
console.log('ok');
