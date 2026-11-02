// Static image renderer: node tools/html2png.mjs <page.html> <out.png|jpg> <width> <height> [scale=1]
// Use for posts / stories / thumbnails built from templates/*.html
import {spawn,execSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
const [,, page,out,wA='1080',hA='1350',sA='1']=process.argv;
if(!page||!out){console.error('usage: node tools/html2png.mjs <page.html> <out.png|jpg> <w> <h> [scale]');process.exit(2)}
const W=+wA,H=+hA,PORT=9333+Math.floor(Math.random()*500);
function findChrome(){
  if(process.env.CHROME)return process.env.CHROME;
  const mac='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if(fs.existsSync(mac))return mac;
  for(const c of ['google-chrome','google-chrome-stable','chromium','chromium-browser']){try{return execSync(`command -v ${c}`).toString().trim()}catch{}}
  throw new Error('Chrome not found. Set CHROME=/path/to/chrome');
}
const chrome=spawn(findChrome(),['--headless=new',`--remote-debugging-port=${PORT}`,'--hide-scrollbars','--force-device-scale-factor=1','--allow-file-access-from-files','--no-first-run',`--window-size=${W},${H}`,`--user-data-dir=${fs.mkdtempSync(path.join(os.tmpdir(),'cr-'))}`,'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let list;for(let i=0;i<80;i++){try{list=await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();if(list.length)break}catch{}await sleep(250)}
const ws=new WebSocket(list.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0;const pend=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}};
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}))});
await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:+sA,mobile:false});
await send('Page.navigate',{url:'file://'+path.resolve(page)});
await sleep(1500);
await send('Runtime.evaluate',{expression:'document.fonts.ready.then(()=>new Promise(r=>setTimeout(r,500)))',awaitPromise:true});
const fmt=out.toLowerCase().endsWith('.jpg')||out.toLowerCase().endsWith('.jpeg')?'jpeg':'png';
const r=await send('Page.captureScreenshot',{format:fmt,quality:95});
fs.mkdirSync(path.dirname(path.resolve(out)),{recursive:true});
fs.writeFileSync(out,Buffer.from(r.result.data,'base64'));
console.log('wrote',out);ws.close();chrome.kill();process.exit(0);
