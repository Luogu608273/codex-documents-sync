const fs = require('fs');
const bytes = fs.readFileSync('work/aha.wasm');
const mod = new WebAssembly.Module(bytes);
console.log('imports', WebAssembly.Module.imports(mod));
console.log('exports', WebAssembly.Module.exports(mod));
const w = new WebAssembly.Instance(mod, {}).exports;
const {createAdapter} = require('./aha.decoded.js');
const a = createAdapter(w, {});
for (const req of [
  {event:'metadata'},
  {event:'init', liveStatus:null, now:1791623000000, state:null, storageBroken:false, search:'', entropy:123456},
  {event:'start'},
  {event:'ended'},
]) {
  console.log(JSON.stringify({request:req,response:a.call(req)},null,2));
}
const strings = [...bytes.toString('utf8').matchAll(/[\x20-\x7e]{6,}/g)].map(x=>x[0]);
fs.writeFileSync('work/wasm-strings.txt',strings.join('\n'));
fs.writeFileSync('work/memory.bin',Buffer.from(w.memory.buffer));
fs.writeFileSync('work/memory-strings.txt', [...Buffer.from(w.memory.buffer).toString('utf8').matchAll(/[\x20-\x7e]{5,}/g)].map(x=>x[0]).join('\n'));
