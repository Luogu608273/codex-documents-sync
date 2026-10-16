const fs = require('fs');
const {createAdapter} = require('./aha.decoded.js');
const mod = new WebAssembly.Module(fs.readFileSync('work/aha.wasm'));
const a = createAdapter(new WebAssembly.Instance(mod, {}).exports, {});
const cases=[];
function call(request){const response=a.call(request);cases.push({request,response});return response;}
call({event:'metadata'});
call({event:'init',search:'?seed=42',state:null,entropy:0});
call({event:'init',search:'?seed=42&force=ur',state:null,entropy:0});
call({event:'start'});
call({event:'playing'});
call({event:'ended'});
for(const event of ['skip','error','timeout']){
  call({event:'init',search:'?seed=42&force=ur',state:null,entropy:0});
  call({event:'start'}); call({event});
}
call({event:'init',search:'?seed=42&probe=1',state:null,entropy:0});
const config=JSON.parse(fs.readFileSync('work/config.json','utf8'));
const boundaries=[];
for(let pity=0;pity<=19;pity++){
 const state={version:2,pity5:pity};
 const r=a.call({event:'compare',search:'?seed=42',state:JSON.stringify(state),count:1});
 boundaries.push({pity5:pity,rate5:r.cards[0].rate5});
}
fs.writeFileSync('work/observations.json',JSON.stringify({cases,boundaries},null,2));
console.log(JSON.stringify({seed42:cases[1].response.commands,boundaries},null,2));
