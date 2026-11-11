const key='iron-journal-v1';
const defaults=()=>({completed:[],last:0,notes:{},plan:{},meals:[],logs:[],measurements:[],photos:[],reviews:[],calculation:null});
let state=defaults();let storageError=false;
try{const raw=JSON.parse(localStorage.getItem(key)||'null');if(raw&&typeof raw==='object'){state={...state,...raw};for(const k of ['completed','meals','logs','measurements','photos','reviews'])if(!Array.isArray(state[k]))state[k]=[];for(const k of ['notes','plan'])if(!state[k]||typeof state[k]!=='object')state[k]={};}}catch{storageError=true;}
export {state,storageError};
export function save(){try{localStorage.setItem(key,JSON.stringify(state));return true;}catch{notify('Storage is unavailable or full. Export a backup before closing this page.');return false;}}
export function notify(message){const el=document.querySelector('#toast');el.textContent=message;el.classList.add('show');clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>el.classList.remove('show'),4200);}
export function download(name,content,type='application/json'){const blob=new Blob([content],{type});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1500);}
export function reset(){Object.assign(state,defaults());return save();}
export function today(){const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;}
