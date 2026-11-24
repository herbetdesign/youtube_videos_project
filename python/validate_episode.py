#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
from scene_generator import validate_episode
p=argparse.ArgumentParser(description='Valida um episodio contra manifest.json.')
p.add_argument('file');a=p.parse_args()
data=json.loads(Path(a.file).read_text(encoding='utf-8'))
errors=validate_episode(data)
if errors:
 print('JSON invalido:');print('\n'.join('- '+e for e in errors));sys.exit(1)
print('JSON valido: personagens, cenarios, objetos, roupas, acessorios e movimentos encontrados.')