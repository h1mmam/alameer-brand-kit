// Deterministic HTML -> JPEG frame renderer (headless Chrome over CDP).
// Usage: node tools/render.mjs <page.html> <framesDir> <outDir> [fps=30] [from=0] [to=86.5] [every=1]
//   env TIMES="1,2.5,10"  -> render only those instants (file names f_<t>.jpg) for previews
//   env CHROME=/path/to/chrome  (defaults: macOS Chrome, then google-chrome / chromium on PATH)
// The page must expose  window.seek(t)  returning a Promise, and read window.FRAMES_DIR / window.COUNTS.
import {spawn,execSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
const [,, page, framesDir, outDir, fpsA='30', fromA='0', toA='86.5', every='1'] = process.argv;
if(!page||!framesDir||!outDir){console.error('usage: node tools/render.mjs <page.html> <framesDir> <outDir> [fps] [from] [to] [every]');process.exit(2)}
const fps=+fpsA, from=+fromA, to=+toA, PORT=9333+Math.floor(Math.random()*500);
const W=+(process.env.W||1080), H=+(process.env.H||1920);
fs.mkdirSync(outDir,{recursive:true});
// frame counts for every clip directory (c1, c2, ... any name)
const counts={};
if(fs.existsSync(framesDir))for(const d of fs.readdirSync(framesDir,{withFileTypes:true}))if(d.isDirectory())
  counts[d.name]=fs.readdirSync(path.join(framesDir,d.name)).filter(f=>f.endsWith('.jpg')).length;
function findChrome(){
  if(process.env.CHROME)return process.env.CHROME;
  const mac='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if(fs.existsSync(mac))return mac;
  for(const c of ['google-chrome','google-chrome-stable','chromium','chromium-browser']){try{return execSync(`command -v ${c}`).toString().trim()}catch{}}
  throw new Error('Chrome not found. Set CHROME=/path/to/chrome');
}
const chrome=spawn(findChrome(),[
 '--headless=new',`--remote-debugging-port=${PORT}`,'--hide-scrollbars','--force-device-scale-factor=1',
 '--allow-file-access-from-files','--no-first-run',`--window-size=${W},${H}`,
 `--user-data-dir=${fs.mkdtempSync(path.join(os.tmpdir(),'cr-'))}`,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let list;for(let i=0;i<80;i++){try{list=await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();if(list.length)break}catch{}await sleep(250)}
const pg=list.find(t=>t.type==='page');
const ws=new WebSocket(pg.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const pend=new Map();
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}};
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:false});
await send('Page.addScriptToEvaluateOnNewDocument',{source:`window.FRAMES_DIR=${JSON.stringify(path.resolve(framesDir))};window.COUNTS=${JSON.stringify(counts)};`});
await send('Page.navigate',{url:'file://'+path.resolve(page)});
await sleep(2500);
await send('Runtime.evaluate',{expression:'document.fonts.ready.then(()=>1)',awaitPromise:true});
const TIMES=process.env.TIMES?process.env.TIMES.split(',').map(Number):null;
const total=TIMES?TIMES.length-1:Math.round((to-from)*fps);
const t0=Date.now();
for(let n=0;n<=total;n+=(TIMES?1:+every)){
  const t=TIMES?TIMES[n]:from+n/fps;
  const r0=await send('Runtime.evaluate',{expression:`seek(${t}).then(()=>1)`,awaitPromise:true});
  if(r0.result?.exceptionDetails){console.error('ERR at',t,JSON.stringify(r0.result.exceptionDetails).slice(0,400));process.exit(1)}
  const r=await send('Page.captureScreenshot',{format:'jpeg',quality:94});
  fs.writeFileSync(path.join(outDir,`f_${TIMES?t.toFixed(2):String(Math.round(t*fps)).padStart(5,'0')}.jpg`),Buffer.from(r.result.data,'base64'));
  if(!TIMES&&n%(fps*5)===0)console.log('t=',t.toFixed(1),'elapsed',((Date.now()-t0)/1000).toFixed(0)+'s');
}
ws.close();chrome.kill();process.exit(0);
