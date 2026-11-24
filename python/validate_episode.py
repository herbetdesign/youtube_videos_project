#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
from scene_generator import validate_episode
p=argparse.ArgumentParser();p.add_argument('file');a=p.parse_args();d=json.loads(Path(a.file).read_text(encoding='utf-8'));e=validate_episode(d)
if e:print('JSON invalido:');print('\n'.join('- '+x for x in e));sys.exit(1)
print('JSON valido: todos os IDs foram encontrados no manifest.json.')
