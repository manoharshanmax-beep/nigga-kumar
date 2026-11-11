export function calculate({age,sex,height,weight,activity,goal}) {
 const values=[age,height,weight,activity].map(Number);if(values.some(n=>!Number.isFinite(n)))throw Error('Enter valid numbers in all fields.');
 if(age<18||age>80||height<120||height>230||weight<35||weight>250)throw Error('This estimator supports adults 18–80, 120–230 cm and 35–250 kg. Seek individual guidance outside those ranges.');
 if(!['male','female'].includes(sex)||![1.2,1.375,1.55,1.725].includes(+activity)||!['gain','maintain','lose'].includes(goal))throw Error('Choose valid options.');
 const bmi=weight/(height/100)**2;if(goal==='lose'&&bmi<18.5)throw Error('A weight-loss target is not appropriate with this low BMI estimate. Choose maintenance and seek individualized guidance.');
 const bmr=10*weight+6.25*height-5*age+(sex==='male'?5:-161),tdee=bmr*activity;
 const target=Math.round(tdee*(goal==='gain'?1.08:goal==='lose'?.9:1));
 if(target<1200)throw Error('This estimate is too low for a general-purpose meal target. Seek personalized guidance.');
 const protein=Math.round(weight*1.6),fat=Math.round(target*.3/9),carbs=Math.round((target-protein*4-fat*9)/4);
 if(carbs<0)throw Error('These inputs need an individualized nutrition plan.');
 return {bmr:Math.round(bmr),tdee:Math.round(tdee),target,protein,fat,carbs,fiber:Math.round(target/1000*14)};
}
export function mealTotals(items,foods){return items.reduce((t,item)=>{const f=foods[item.food];if(!f||!Number.isFinite(+item.grams)||item.grams<=0)return t;const q=item.grams/100;return t.map((n,i)=>n+(i===5?item.price??f[7]:f[i+2])*q)},[0,0,0,0,0,0]);}
export function weeklyMean(rows){if(!rows.length)return null;return rows.reduce((s,r)=>s+Number(r.weight),0)/rows.length;}
export const escapeHtml=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
