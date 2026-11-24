(() => {
  const qs = new URLSearchParams(location.search);
  const episodeUrl = qs.get('episode') || '../examples/episode_001.json';
  const $ = (id) => document.getElementById(id);
  const stage = $('stage'), camera = $('camera-layer'), background = $('background');
  const objectLayer = $('object-layer'), characterLayer = $('character-layer'), overlayLayer = $('overlay-layer');
  let episode=null, currentTime=0, playing=false, lastTick=0, raf=0, sceneCache=new Map(), charCache=new Map();
  const assetPath = (kind,id) => `../${kind}/${id}${kind==='characters' ? '/character.svg' : '.svg'}`;
  async function loadSvg(path, cache){
    if(cache.has(path)) return cache.get(path).cloneNode(true);
    const response=await fetch(path); if(!response.ok) throw new Error(`Não foi possível carregar ${path}`);
    const text=await response.text(); const doc=new DOMParser().parseFromString(text,'image/svg+xml');
    const root=doc.documentElement; const node=root.querySelector('#character-rig') || root.querySelector('g') || root;
    cache.set(path,node.cloneNode(true)); return node.cloneNode(true);
  }
  function clear(node){while(node.firstChild) node.removeChild(node.firstChild)}
  function addImage(parent, href, x,y,w,h,rotate=0){const im=document.createElementNS('http://www.w3.org/2000/svg','image');im.setAttribute('href',href);im.setAttribute('x',x);im.setAttribute('y',y);im.setAttribute('width',w);im.setAttribute('height',h);if(rotate)im.setAttribute('transform',`rotate(${rotate} ${x+w/2} ${y+h/2})`);parent.appendChild(im)}
  function activeScene(t){let sum=0;for(let i=0;i<episode.scenes.length;i++){const s=episode.scenes[i];if(t<sum+s.duration_seconds)return {scene:s,index:i,local:t-sum,start:sum};sum+=s.duration_seconds;}const s=episode.scenes.at(-1);return {scene:s,index:episode.scenes.length-1,local:s.duration_seconds,start:sum-s.duration_seconds};}
  function movementTransform(move, t){const a=t*2*Math.PI;switch(move){case'talking':return `translate(0 ${Math.sin(a*2)*3})`;case'typing':return `translate(${Math.sin(a*2)*2} ${Math.abs(Math.sin(a*2))*3})`;case'thinking':return `rotate(${Math.sin(a)*1.7} 300 600) translate(0 ${Math.sin(a)*2})`;case'walking':return `translate(${Math.sin(a*2)*10} ${Math.abs(Math.sin(a*2))*-7})`;case'pointing':return `translate(0 ${Math.sin(a)*3})`;case'celebrating':return `translate(0 ${Math.abs(Math.sin(a*2))*-12})`;case'holding_phone':return `rotate(${Math.sin(a)*1.2} 300 620) translate(0 ${Math.sin(a)*2})`;case'holding_money':return `translate(0 ${Math.abs(Math.sin(a))*2})`;case'writing':return `rotate(${Math.sin(a*2)*0.8} 300 620) translate(0 ${Math.abs(Math.sin(a*2))*2})`;default:return `translate(0 ${Math.sin(a)*1.3})`;}}
  async function renderAt(t){
    if(!episode)return;currentTime=Math.max(0,Math.min(t,totalDuration()));const active=activeScene(currentTime),s=active.scene,local=active.local;
    background.setAttribute('href',`../scenes/${s.background}.svg`);
    clear(objectLayer);clear(characterLayer);clear(overlayLayer);
    for(const obj of (s.objects||[])){const p=obj;const w=p.width||180,h=p.height||180,x=(p.x??.8)*1920-w/2,y=(p.y??.65)*1080-h/2;addImage(objectLayer,`../objects/${p.id}.svg`,x,y,w,h,p.rotate||0);}
    const c=await loadSvg(assetPath('characters',s.character),charCache);const pos=s.position||{x:.5,y:.68,scale:1};const cx=(pos.x??.5)*1920,cy=(pos.y??.68)*1080,scale=(pos.scale??1)*1.03;
    c.setAttribute('transform',`translate(${cx} ${cy}) scale(${scale}) translate(-300 -360) ${movementTransform(s.movement,local)}`);
    c.querySelectorAll('.face-expression').forEach(g=>g.style.display=g.getAttribute('data-expression')===s.expression?'inline':'none');
    const activeFace=c.querySelector(`.face-expression[data-expression="${s.expression}"]`);
    if(activeFace){const paths=activeFace.querySelectorAll('path');const mouth=paths[paths.length-1];if(mouth){const base=mouth.getAttribute('d');if(s.movement==='talking' && Math.sin(local*8)>0){mouth.setAttribute('d','M276 294 Q300 280 324 294 Q334 342 300 346 Q266 342 276 294');}else{mouth.setAttribute('d',base);}}}
    characterLayer.appendChild(c);
    const caption=s.text_overlay||'';if(caption){const text=document.createElementNS('http://www.w3.org/2000/svg','text');text.setAttribute('x','960');text.setAttribute('y','980');text.setAttribute('text-anchor','middle');text.setAttribute('font-size','48');text.setAttribute('class','scene-caption');text.textContent=caption;overlayLayer.appendChild(text);}
    let zoom=1,dx=0;if(s.camera==='slow_zoom_in')zoom=1+0.05*(local/(s.duration_seconds||1));if(s.camera==='slow_zoom_out')zoom=1.05-0.05*(local/(s.duration_seconds||1));if(s.camera==='pan_left')dx=30*(local/(s.duration_seconds||1));if(s.camera==='pan_right')dx=-30*(local/(s.duration_seconds||1));camera.setAttribute('transform',`translate(${dx} 0) translate(960 540) scale(${zoom}) translate(-960 -540)`);
    $('episode-title').textContent=episode.title||episode.episode_id;$('scene-label').textContent=`Cena ${active.index+1}/${episode.scenes.length} — ${s.id}`;$('time-label').textContent=`${fmt(currentTime)} / ${fmt(totalDuration())}`;$('progress').style.width=`${100*currentTime/totalDuration()}%`;
  }
  function totalDuration(){return episode.scenes.reduce((n,s)=>n+Number(s.duration_seconds||0),0)}function fmt(s){const m=Math.floor(s/60),sec=Math.floor(s%60);return `${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`}
  async function tick(now){if(!playing)return;if(!lastTick)lastTick=now;const dt=Math.min(.1,(now-lastTick)/1000);lastTick=now;await renderAt(currentTime+dt);if(currentTime>=totalDuration()){playing=false;$('play').textContent='▶ Reproduzir';return;}raf=requestAnimationFrame(tick)}
  async function init(){const r=await fetch(episodeUrl);if(!r.ok)throw new Error(`Episódio não encontrado: ${episodeUrl}`);episode=await r.json();await renderAt(0);window.engineReady=true;}
  $('play').addEventListener('click',()=>{playing=!playing;if(playing){lastTick=0;$('play').textContent='Ⅱ Pausar';raf=requestAnimationFrame(tick);}else{$('play').textContent='▶ Reproduzir';cancelAnimationFrame(raf);}});
  $('prev').addEventListener('click',async()=>{if(!episode)return;const a=activeScene(currentTime);await renderAt(Math.max(0,a.start-0.05));});
  $('next').addEventListener('click',async()=>{if(!episode)return;const a=activeScene(currentTime);await renderAt(Math.min(totalDuration(),a.start+episode.scenes[a.index].duration_seconds+0.01));});
  window.renderAt=renderAt;window.getEpisode=()=>episode;window.getDuration=totalDuration;
  init().catch(e=>{console.error(e);$('episode-title').textContent='Erro: '+e.message;});
})();
