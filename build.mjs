import fs from 'node:fs';import {execFileSync} from 'node:child_process';
for(const f of fs.readdirSync('dist').filter(f=>f.endsWith('.js')))execFileSync(process.execPath,['--check','dist/'+f]);
execFileSync(process.execPath,['scripts/test.mjs'],{stdio:'inherit'});
const h=JSON.parse(fs.readFileSync('.openai/hosting.json'));if(h.static?.directory!=='dist')throw Error('Invalid static output');
console.log('Production static build validated. No runtime build or external JS dependency is required.');
