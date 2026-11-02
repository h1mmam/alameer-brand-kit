// Usage: node render.mjs <outDir> <fps> <from_s> <to_s> [step_frames]
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const [,, outDir, fpsA='30', fromA='0', toA='56', every='1'] = process.argv;
const fps=+fpsA, from=+fromA, to=+toA, PORT=9333+Math.floor(Math.random()*500);
fs.mkdirSync(outDir,{recursive:true});
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',[
 '--headless=new',`--remote-debugging-port=${PORT}`,'--hide-scrollbars','--force-device-scale-factor=1',
 '--allow-file-access-from-files','--disable-gpu-vsync','--no-first-run','--window-size=1080,1920',
 `--user-data-dir=${fs.mkdtempSync('/tmp/cr-')}`,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let list;for(let i=0;i<60;i++){try{list=await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();if(list.length)break}catch{}await sleep(250)}
const page=list.find(t=>t.type==='page');
const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const pend=new Map();
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}};
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride',{width:1080,height:1920,deviceScaleFactor:1,mobile:false});
await send('Page.navigate',{url:'file://'+path.resolve('index.html')});
await sleep(2500);
await send('Runtime.evaluate',{expression:'document.fonts.ready.then(()=>1)',awaitPromise:true});
const total=Math.round((to-from)*fps);
for(let n=0;n<=total;n+=(+every)){
  const t=from+n/fps;
  await send('Runtime.evaluate',{expression:`seek(${t})`});
  const r=await send('Page.captureScreenshot',{format:'jpeg',quality:93});
  fs.writeFileSync(path.join(outDir,`f_${String(Math.round(t*fps)).padStart(5,'0')}.jpg`),Buffer.from(r.result.data,'base64'));
  if(n%(fps*4)===0)console.log('t=',t.toFixed(1));
}
ws.close();chrome.kill();process.exit(0);
