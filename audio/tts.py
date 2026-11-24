#!/usr/bin/env python3
"""Offline TTS helper using installed Windows/system voices via pyttsx3."""
import argparse, json
from pathlib import Path
import pyttsx3
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--episode',default=str(ROOT/'examples'/'episode_001.json'))
p.add_argument('--output',default=str(ROOT/'output'/'audio'/'narration.wav'))
p.add_argument('--rate',type=int,default=160)
p.add_argument('--voice-contains',default='',help='Optional substring to select an installed voice, e.g. Portuguese or Brasil.')
a=p.parse_args(); data=json.loads(Path(a.episode).read_text(encoding='utf-8'))
engine=pyttsx3.init(); engine.setProperty('rate',a.rate)
voices=engine.getProperty('voices')
if a.voice_contains:
    match=next((v for v in voices if a.voice_contains.lower() in (v.name+' '+str(v.id)).lower()),None)
    if not match: raise SystemExit('Nenhuma voz instalada corresponde ao filtro informado.')
    engine.setProperty('voice',match.id)
lines=[s.get('narration','').strip() for s in data['scenes'] if s.get('narration','').strip()]
if not lines: raise SystemExit('Nenhum texto de narração foi encontrado no episódio.')
out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
engine.save_to_file(' '.join(lines),str(out)); engine.runAndWait()
print(f'Áudio salvo em {out}. Confira a voz e a pronúncia antes de publicar.')
