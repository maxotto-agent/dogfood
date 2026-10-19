// Energy maths. RER and life-stage factors: Ohio State University Veterinary Medical Center, "Basic calorie calculator", Table 1.
const FACTORS = {
  neutered: ['Neutered adult', 1.6],
  intact: ['Intact adult', 1.8],
  inactive: ['Inactive or prone to obesity', 1.3],
  puppy4: ['Puppy under 4 months', 3.0],
  puppy12: ['Puppy 4 months to adult', 2.0],
};
function rer(kg) { return 70 * Math.pow(kg, 0.75); }
function mer(kg, stage) { return rer(kg) * FACTORS[stage][1]; }
function portions(kcal, food) {
  return { cups: kcal / food.kcal_cup, grams: kcal / food.kcal_kg * 1000 };
}
// Cups of the new food that match the calories of the old amount.
function switchCups(oldCups, oldKcalCup, newKcalCup) {
  const kcal = oldCups * oldKcalCup;
  return { kcal, cups: kcal / newKcalCup, change: newKcalCup / oldKcalCup - 1 };
}
// 7-day mix, each day's total equals `kcal`. Share of new food per day.
const MIX = [0.25, 0.25, 0.5, 0.5, 0.75, 0.75, 1];
function mixPlan(kcal, oldKcalCup, newKcalCup) {
  return MIX.map((s, i) => ({ day: i + 1, share: s, newCups: kcal * s / newKcalCup, oldCups: kcal * (1 - s) / oldKcalCup }));
}
const FRACS = ['', '1/8', '1/4', '3/8', '1/2', '5/8', '3/4', '7/8'];
function fmtCups(c) {
  const eighths = Math.round(c * 8), w = Math.floor(eighths / 8), f = FRACS[eighths % 8];
  if (!w && !f) return '0';
  return (w ? w : '') + (w && f ? ' ' : '') + f;
}
if (typeof module !== 'undefined') module.exports = { FACTORS, rer, mer, portions, switchCups, mixPlan, fmtCups };
