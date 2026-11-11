import assert from 'node:assert/strict';
import {calculate,mealTotals,escapeHtml} from '../dist/core.js';
import {chapters,exercises,foods,muscles} from '../dist/data.js';
import fs from 'node:fs';
const base={age:25,sex:'male',height:175,weight:70,activity:1.55,goal:'maintain'};
const r=calculate(base);assert.equal(r.bmr,1674);assert.equal(r.tdee,2594);assert.equal(r.target,2594);assert.equal(r.protein,112);assert.ok(Math.abs(r.protein*4+r.fat*9+r.carbs*4-r.target)<=5);
assert.equal(calculate({...base,sex:'female'}).bmr,1508);assert.equal(calculate({...base,goal:'gain'}).target,2802);assert.equal(calculate({...base,goal:'lose'}).target,2335);
for(const patch of [{age:17},{height:0},{weight:NaN},{activity:7},{sex:'x'},{goal:'x'},{weight:40,goal:'lose'}])assert.throws(()=>calculate({...base,...patch}));
assert.deepEqual(mealTotals([],foods),[0,0,0,0,0,0]);const total=mealTotals([{food:0,grams:200,price:10},{food:4,grams:100,price:35}],foods);assert.equal(total[0],425);assert.equal(total[1],36.4);assert.equal(total[5],55);
assert.equal(escapeHtml('<img src=x onerror="x">'),'&lt;img src=x onerror=&quot;x&quot;&gt;');
assert.equal(chapters.length,13);assert.equal(muscles.length,11);assert.equal(exercises.length,18);
for(const [i,c] of chapters.entries()){assert.ok(c.lessons.length>=3);assert.ok(c.quiz[2]>=0&&c.quiz[2]<c.quiz[1].length);assert.ok(c.refs.length);const file=`dist/docs/chapter-${String(i).padStart(2,'0')}.pdf`;assert.ok(fs.statSync(file).size>10000);assert.equal(fs.readFileSync(file).subarray(0,4).toString(),'%PDF');}
for(const x of exercises){assert.equal(x.length,11);assert.ok(x.every(v=>v.length>0));}
for(const f of ['index.html','404.html','assets/favicon.svg','assets/hero.webp','assets/three.module.js','assets/gsap.min.js','assets/ScrollTrigger.min.js'])assert.ok(fs.existsSync('dist/'+f));
console.log('PASS: calculator reference cases and invalid inputs, macro energy balance, meal quantities and prices, escaping, 13 complete chapters, 18 exercises, 11 muscle regions, 13 PDF files and required assets.');
