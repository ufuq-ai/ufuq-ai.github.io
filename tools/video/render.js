const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const FPS=30,CH=10;const which=process.argv.slice(2).map(Number);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('file://'+__dirname+'/stage.html');await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));
for(const c of which){const tmp=`chunks/c${c}.tmp.mp4`,out=`chunks/c${c}.mp4`;const t0=Date.now();
 const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r',String(FPS),tmp]);
 const done=new Promise(r=>ff.on('close',r));ff.stderr.on('data',d=>process.stderr.write(d));
 for(let i=0;i<CH*FPS;i++){const t=c*CH+i/FPS;await p.evaluate(t=>render(t),t);const buf=await p.screenshot({type:'jpeg',quality:92});
  if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
 ff.stdin.end();const code=await done;if(code===0)fs.renameSync(tmp,out);console.log('chunk',c,'exit',code,((Date.now()-t0)/1000).toFixed(0)+'s');}
console.log('errors',errs);await b.close();})();
