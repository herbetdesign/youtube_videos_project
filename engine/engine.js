(() => {
  const qs=new URLSearchParams(location.search),episodeUrl=qs.get('episode')||'../examples/episode_001.json';
  const $=id=>document.getElementById(id),stage=$('stage'),camera=$('camera-layer'),background=$('background'),objectLayer=$('object-layer'),characterLayer=$('character-layer'),overlayLayer=$('overlay-layer');
  let episode=null,currentTime=0,playing=false,lastTick=0,raf=0,charCache=new Map(),duration=0;
  const ns='http://www.w3.org/2000/svg';
  async function loadRig(id){
    const path='../characters/'+id+'/character.svg';
    if(charCache.has(path))return charCache.get(path).cloneNode(true);
    const res=await fetch(path);if(!res.ok)throw new Error('Personagem não encontrado: '+id);
    const doc=new DOMParser().parseFromString(await res.text(),'image/svg+xml');
    const rig=doc.querySelector('#character-rig');if(!rig)throw new Error('SVG sem #character-rig: '+id);
    charCache.set(path,rig.cloneNode(true));return rig.cloneNode(true);
  }
  function clear(n){while(n.firstChild)n.removeChild(n.firstChild)}
  function image(parent,href,x,y,w,h,rotate=0){const el=document.createElementNS(ns,'image');el.setAttribute('href',href);el.setAttribute('x',x);el.setAttribute('y',y);el.setAttribute('width',w);el.setAttribute('height',h);if(rotate)el.setAttribute('transform',`rotate(${rotate} ${x+w/2} ${y+h/2})`);parent.appendChild(el);return el}
  function total(){return duration}
  function fmt(v){const m=Math.floor(v/60),s=Math.floor(v%60);return String(m).padStart(2,'0')+':'+String(s).padStart(2,'0')}
  function findScene(t){let start=0;for(let i=0;i<episode.scenes.length;i++){const s=episode.scenes[i],d=Number(s.duration_seconds);if(t<start+d)return{scene:s,index:i,local:t-start,start};start+=d}const i=episode.scenes.length-1;return{scene:episode.scenes[i],index:i,local:Number(episode.scenes[i].duration_seconds),start:duration-Number(episode.scenes[i].duration_seconds)}}
  function joint(rig,id,angle,x,y){const el=rig.querySelector('#'+id);if(el)el.setAttribute('transform',angle?`rotate(${angle} ${x} ${y})`:'')}
  function pose(rig,move,t){
    const w=Math.sin(t*6),fast=Math.sin(t*12);
    let al=0,ar=0,ll=0,lr=0,head=0,torso=0;
    if(move==='talking'){ar=-18+w*10;al=10-w*7;head=w*2}
    if(move==='typing'){al=-8+fast*4;ar=8-fast*4;head=fast*1}
    if(move==='thinking'){al=38;head=-8+w*2}
    if(move==='walking'){al=25*w;ar=-25*w;ll=-26*w;lr=26*w;torso=Math.abs(w)*2}
    if(move==='running'){al=48*fast;ar=-48*fast;ll=-42*fast;lr=42*fast;torso=Math.abs(fast)*4}
    if(move==='pointing'){ar=-67+w*2;head=-3}
    if(move==='celebrating'){al=125;ar=-125;ll=-8*w;lr=8*w;torso=-Math.abs(w)*3}
    if(move==='holding_phone'){al=-42;head=6+Math.sin(t*2)*2}
    if(move==='holding_money'){ar=-46;head=-4}
    if(move==='writing'){ar=-24+fast*5;head=5}
    if(move==='idle'){head=w*1.3;torso=Math.abs(w)*1.3}
    joint(rig,'arm-left',al,115,195);joint(rig,'arm-right',ar,285,195);
    joint(rig,'leg-left',ll,165,365);joint(rig,'leg-right',lr,235,365);
    joint(rig,'head',head,200,150);const b=rig.querySelector('#torso');if(b)b.setAttribute('transform',torso?`translate(0 ${torso})`:'');
    const face=rig.querySelectorAll('.face-expression');face.forEach(g=>g.style.display=g.getAttribute('data-expression')===rig.__expression?'inline':'none');
  }
  async function renderAt(t){
    if(!episode)return;currentTime=Math.max(0,Math.min(t,duration));const a=findScene(currentTime),s=a.scene,local=a.local;
    background.setAttribute('href','../scenes/'+s.background+'.svg');clear(objectLayer);clear(characterLayer);clear(overlayLayer);
    for(const obj of (s.objects||[])){const w=obj.width||170,h=obj.height||170,x=(obj.x??.8)*1920-w/2,y=(obj.y??.68)*1080-h/2;image(objectLayer,'../objects/'+obj.id+'.svg',x,y,w,h,obj.rotate||0);}
    const rig=await loadRig(s.character),pos=s.position||{x:.5,y:.91,scale:1},scale=Number(pos.scale||1),cx=(pos.x??.5)*1920,baseY=(pos.y??.91)*1080;
    rig.__expression=s.expression||'neutral';pose(rig,s.movement||'idle',local);
    rig.setAttribute('transform',`translate(${cx} ${baseY}) scale(${scale}) translate(-200 -540)`);
    if(s.outfit){const el=document.createElementNS(ns,'image');el.setAttribute('href','../outfits/'+s.outfit+'.svg');el.setAttribute('x',0);el.setAttribute('y',0);el.setAttribute('width',400);el.setAttribute('height',560);rig.appendChild(el);}
    for(const acc of (s.accessories||[])){const el=document.createElementNS(ns,'image');el.setAttribute('href','../accessories/'+acc+'.svg');el.setAttribute('x',0);el.setAttribute('y',0);el.setAttribute('width',400);el.setAttribute('height',560);rig.appendChild(el);}
    characterLayer.appendChild(rig);
    if(s.text_overlay){const tx=document.createElementNS(ns,'text');tx.setAttribute('x',960);tx.setAttribute('y',1000);tx.setAttribute('text-anchor','middle');tx.setAttribute('font-family','Arial,sans-serif');tx.setAttribute('font-size','54');tx.setAttribute('font-weight','900');tx.setAttribute('fill','#FFFFFF');tx.setAttribute('stroke','#20252B');tx.setAttribute('stroke-width','13');tx.setAttribute('paint-order','stroke');tx.textContent=s.text_overlay;overlayLayer.appendChild(tx);}
    let zoom=1,dx=0;if(s.camera==='slow_zoom_in')zoom=1+.05*local/s.duration_seconds;if(s.camera==='slow_zoom_out')zoom=1.05-.05*local/s.duration_seconds;if(s.camera==='pan_left')dx=30*local/s.duration_seconds;if(s.camera==='pan_right')dx=-30*local/s.duration_seconds;
    camera.setAttribute('transform',`translate(${dx} 0) translate(960 540) scale(${zoom}) translate(-960 -540)`);
    $('episode-title').textContent=episode.title||episode.episode_id;$('scene-label').textContent='Cena '+(a.index+1)+'/'+episode.scenes.length+' — '+s.id;$('time-label').textContent=fmt(currentTime)+' / '+fmt(duration);$('progress').style.width=(100*currentTime/duration)+'%';
  }
  async function tick(now){if(!playing)return;if(!lastTick)lastTick=now;const dt=Math.min(.1,(now-lastTick)/1000);lastTick=now;await renderAt(currentTime+dt);if(currentTime>=duration){playing=false;$('play').textContent='▶ Reproduzir';return}raf=requestAnimationFrame(tick)}
  async function init(){const r=await fetch(episodeUrl);if(!r.ok)throw new Error('Episódio não encontrado: '+episodeUrl);episode=await r.json();duration=episode.scenes.reduce((n,s)=>n+Number(s.duration_seconds),0);await renderAt(0);window.engineReady=true}
  $('play').addEventListener('click',()=>{playing=!playing;if(playing){lastTick=0;$('play').textContent='Ⅱ Pausar';raf=requestAnimationFrame(tick)}else{$('play').textContent='▶ Reproduzir';cancelAnimationFrame(raf)}});
  $('prev').addEventListener('click',async()=>{if(!episode)return;const a=findScene(currentTime);await renderAt(Math.max(0,a.start-.01))});
  $('next').addEventListener('click',async()=>{if(!episode)return;const a=findScene(currentTime);await renderAt(Math.min(duration,a.start+Number(a.scene.duration_seconds)+.01))});
  window.renderAt=renderAt;window.getDuration=total;init().catch(e=>{$('episode-title').textContent='Erro: '+e.message;console.error(e)});
})();