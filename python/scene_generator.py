#!/usr/bin/env python3
import argparse,json,os,sys,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];M=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def validate_episode(d):
 e=[]
 if not isinstance(d,dict):return ['Episodio precisa ser objeto JSON.']
 for k in ('episode_id','title','resolution','fps','scenes'):
  if k not in d:e.append('Campo ausente: '+k)
 if d.get('resolution')!={'width':1920,'height':1080}:e.append('resolution deve ser 1920x1080.')
 if not isinstance(d.get('scenes'),list) or not d.get('scenes'):e.append('scenes precisa ser lista nao vazia.');return e
 known={'background':set(M['scenes']),'character':set(M['characters']),'expression':set(M['expressions']),'movement':set(M['movements']),'camera':set(M['camera'])};ids=set()
 for i,s in enumerate(d['scenes'],1):
  if not isinstance(s,dict):e.append(f'Cena {i}: objeto invalido.');continue
  for k in ('id','duration_seconds','background','character','expression','movement','narration'):
   if k not in s:e.append(f'Cena {i}: campo ausente {k}.')
  if s.get('id') in ids:e.append(f'Cena {i}: ID duplicado.')
  ids.add(s.get('id'))
  for k,v in known.items():
   if s.get(k,'static' if k=='camera' else None) not in v:e.append(f'Cena {i}: {k} desconhecido: {s.get(k)}.')
  if s.get('outfit') and s['outfit'] not in M['outfits']:e.append(f'Cena {i}: roupa desconhecida.')
  for a in s.get('accessories',[]):
   if a not in M['accessories']:e.append(f'Cena {i}: acessorio desconhecido: {a}.')
  try:
   if float(s.get('duration_seconds',0))<=0:e.append(f'Cena {i}: duracao deve ser positiva.')
  except (TypeError,ValueError):e.append(f'Cena {i}: duracao invalida.')
  for o in s.get('objects',[]):
   if o.get('id') not in M['objects']:e.append(f'Cena {i}: objeto desconhecido {o.get("id")}.')
 return e
def ask(story,model,url):
 prompt='Converta storyboard em JSON para o kit 2D Blocky. Use somente IDs deste catalogo. Campos do episodio: episode_id,title,resolution {width:1920,height:1080},fps,scenes. Campos por cena: id,duration_seconds,background,character,expression,movement,position{x,y,scale},outfit opcional,accessories opcional,objects[{id,x,y,width,height}],camera,text_overlay,narration. Retorne JSON. Catalogo: '+json.dumps(M,ensure_ascii=False)
 body={'model':model,'stream':False,'format':'json','messages':[{'role':'system','content':prompt},{'role':'user','content':story}]};req=urllib.request.Request(url.rstrip('/')+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=300) as r:return json.loads(json.loads(r.read().decode()).get('message',{}).get('content','{}'))
 except urllib.error.URLError as ex:raise RuntimeError(f'Falha no Ollama: {ex}') from ex
def main():
 p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--storyboard');p.add_argument('--output',default=str(ROOT/'output'/'episode.json'));p.add_argument('--model',default=os.getenv('OLLAMA_MODEL','qwen2.5:3b'));p.add_argument('--endpoint',default=os.getenv('OLLAMA_URL','http://localhost:11434'));a=p.parse_args()
 if not a.input and not a.storyboard:p.error('Informe --input ou --storyboard.')
 d=json.loads(Path(a.input).read_text(encoding='utf-8')) if a.input else ask(Path(a.storyboard).read_text(encoding='utf-8'),a.model,a.endpoint)
 errors=validate_episode(d)
 if errors:print('\n'.join(errors),file=sys.stderr);return 1
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');print('Episodio salvo:',out);return 0
if __name__=='__main__':raise SystemExit(main())
