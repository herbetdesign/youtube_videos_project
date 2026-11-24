#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
def validate_episode(data):
 errors=[]
 if not isinstance(data,dict): return ['Episodio precisa ser um objeto JSON.']
 for k in ('episode_id','title','resolution','fps','scenes'):
  if k not in data: errors.append('Campo obrigatorio ausente: '+k)
 if data.get('resolution')!={'width':1920,'height':1080}: errors.append('resolution deve ser 1920x1080.')
 if not isinstance(data.get('scenes'),list) or not data.get('scenes'): errors.append('scenes deve ser lista nao vazia.');return errors
 known={'background':set(MANIFEST['scenes']),'character':set(MANIFEST['characters']),'expression':set(MANIFEST['expressions']),'movement':set(MANIFEST['movements']),'outfit':set(MANIFEST['outfits']),'camera':set(MANIFEST['camera'])}
 ids=set()
 for i,s in enumerate(data['scenes'],1):
  if not isinstance(s,dict): errors.append(f'Cena {i}: objeto invalido.');continue
  for f in ('id','duration_seconds','background','character','expression','movement','narration'):
   if f not in s: errors.append(f'Cena {i}: campo ausente {f}.')
  if s.get('id') in ids: errors.append(f'Cena {i}: ID duplicado {s.get("id")}.')
  ids.add(s.get('id'))
  for f,valid in known.items():
   if f=='outfit' and not s.get(f): continue
   if s.get(f,'static' if f=='camera' else None) not in valid: errors.append(f'Cena {i}: {f} desconhecido: {s.get(f)}.')
  for acc in s.get('accessories',[]):
   if acc not in MANIFEST['accessories']: errors.append(f'Cena {i}: acessorio desconhecido: {acc}.')
  try:
   if float(s.get('duration_seconds',0))<=0: errors.append(f'Cena {i}: duration_seconds deve ser positivo.')
  except (ValueError,TypeError): errors.append(f'Cena {i}: duration_seconds deve ser numerico.')
  for obj in s.get('objects',[]):
   if obj.get('id') not in MANIFEST['objects']: errors.append(f'Cena {i}: objeto desconhecido: {obj.get("id")}.')
 return errors
def ask_ollama(storyboard,model,endpoint):
 prompt='Converta o storyboard em JSON para Financial Animation Kit 2D Blocky. Use somente IDs do catalogo abaixo. Retorne apenas JSON. Cada cena precisa id,duration_seconds,background,character,expression,movement,position{x,y,scale},objects[{id,x,y,width,height}],camera,text_overlay,narration. Outfit e accessories sao opcionais. Resolucao 1920x1080. Catalogo: '+json.dumps(MANIFEST,ensure_ascii=False)
 body={'model':model,'stream':False,'format':'json','messages':[{'role':'system','content':prompt},{'role':'user','content':storyboard}]}
 req=urllib.request.Request(endpoint.rstrip('/')+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=300) as r: result=json.loads(r.read().decode())
 except urllib.error.URLError as e: raise RuntimeError(f'Falha no Ollama: {e}') from e
 return json.loads(result.get('message',{}).get('content','{}'))
def main():
 p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--storyboard');p.add_argument('--output',default=str(ROOT/'output'/'episode.json'));p.add_argument('--model',default=os.getenv('OLLAMA_MODEL','qwen2.5:3b'));p.add_argument('--endpoint',default=os.getenv('OLLAMA_URL','http://localhost:11434'));a=p.parse_args()
 if not a.input and not a.storyboard:p.error('Informe --input ou --storyboard.')
 data=json.loads(Path(a.input).read_text(encoding='utf-8')) if a.input else ask_ollama(Path(a.storyboard).read_text(encoding='utf-8'),a.model,a.endpoint)
 errors=validate_episode(data)
 if errors:print('\n'.join('ERRO: '+e for e in errors),file=sys.stderr);return 1
 out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print('Episodio salvo em '+str(out));return 0
if __name__=='__main__':raise SystemExit(main())
