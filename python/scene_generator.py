#!/usr/bin/env python3
"Generate or validate scene JSON using the local Ollama API."
from __future__ import annotations
import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))

def validate_episode(data: dict) -> list[str]:
    errors=[]
    if not isinstance(data,dict): return ['O episódio precisa ser um objeto JSON.']
    for key in ('episode_id','title','resolution','fps','scenes'):
        if key not in data: errors.append(f'Campo obrigatório ausente: {key}')
    if data.get('resolution') != {'width':1920,'height':1080}:
        errors.append('resolution deve ser exatamente {"width": 1920, "height": 1080}.')
    if not isinstance(data.get('scenes'),list) or not data.get('scenes'):
        errors.append('scenes precisa ser uma lista com pelo menos uma cena.')
        return errors
    known_bg=set(MANIFEST['scenes']); known_char=set(MANIFEST['characters']); known_obj=set(MANIFEST['objects'])
    known_expr=set(MANIFEST['expressions']); known_move=set(MANIFEST['movements']); known_cam=set(MANIFEST['camera'])
    ids=set()
    for i,s in enumerate(data['scenes'],1):
        prefix=f'Cena {i}'
        if not isinstance(s,dict): errors.append(f'{prefix}: deve ser um objeto.'); continue
        for k in ('id','duration_seconds','background','character','expression','movement','narration'):
            if k not in s: errors.append(f'{prefix}: campo ausente: {k}')
        if s.get('id') in ids: errors.append(f'{prefix}: ID duplicado: {s.get("id")}')
        ids.add(s.get('id'))
        if s.get('background') not in known_bg: errors.append(f'{prefix}: cenário desconhecido: {s.get("background")}')
        if s.get('character') not in known_char: errors.append(f'{prefix}: personagem desconhecido: {s.get("character")}')
        if s.get('expression') not in known_expr: errors.append(f'{prefix}: expressão desconhecida: {s.get("expression")}')
        if s.get('movement') not in known_move: errors.append(f'{prefix}: movimento desconhecido: {s.get("movement")}')
        if s.get('camera','static') not in known_cam: errors.append(f'{prefix}: câmera desconhecida: {s.get("camera")}')
        try:
            if float(s.get('duration_seconds',0)) <= 0: errors.append(f'{prefix}: duration_seconds deve ser maior que zero.')
        except (TypeError,ValueError): errors.append(f'{prefix}: duration_seconds deve ser numérico.')
        for obj in s.get('objects',[]):
            if obj.get('id') not in known_obj: errors.append(f'{prefix}: objeto desconhecido: {obj.get("id")}')
    return errors

def ask_ollama(storyboard: str, model: str, endpoint: str) -> dict:
    prompt = '''Converta o storyboard fornecido em JSON para o motor Financial Animation Kit. Use SOMENTE IDs que existam no catálogo abaixo. Não invente personagens, cenários, objetos, expressões, movimentos ou câmeras. Retorne apenas JSON válido, sem Markdown. Campos obrigatórios do episódio: episode_id, title, description, resolution {width:1920,height:1080}, fps:15, scenes. Cada cena precisa de id, duration_seconds, background, character, expression, movement, position {x,y,scale}, objects [{id,x,y,width,height}], camera, text_overlay, narration. Coordenadas x/y são normalizadas entre 0 e 1. Catálogo:\n''' + json.dumps(MANIFEST,ensure_ascii=False)
    body={'model':model,'stream':False,'format':'json','messages':[{'role':'system','content':prompt},{'role':'user','content':storyboard}]}
    req=urllib.request.Request(endpoint.rstrip('/')+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=300) as response: result=json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as exc: raise RuntimeError(f'Não foi possível acessar o Ollama em {endpoint}: {exc}') from exc
    content=result.get('message',{}).get('content','')
    try: return json.loads(content)
    except json.JSONDecodeError as exc: raise RuntimeError(f'O Ollama não retornou JSON válido: {content[:500]}') from exc

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',help='Arquivo JSON já criado pelo ChatGPT para validar.')
    p.add_argument('--storyboard',help='Arquivo .txt ou .md com storyboard para converter via Ollama.')
    p.add_argument('--output',default=str(ROOT/'output'/'episode.json'))
    p.add_argument('--model',default=os.getenv('OLLAMA_MODEL','qwen2.5:3b'))
    p.add_argument('--endpoint',default=os.getenv('OLLAMA_URL','http://localhost:11434'))
    args=p.parse_args()
    if not args.input and not args.storyboard: p.error('Informe --input ou --storyboard.')
    if args.input: data=json.loads(Path(args.input).read_text(encoding='utf-8'))
    else: data=ask_ollama(Path(args.storyboard).read_text(encoding='utf-8'),args.model,args.endpoint)
    errors=validate_episode(data)
    if errors:
        print('\n'.join('ERRO: '+e for e in errors),file=sys.stderr); return 1
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Episódio validado e salvo em: {out}')
    return 0
if __name__=='__main__': raise SystemExit(main())
