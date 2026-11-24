#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path
from scene_generator import validate_episode
p=argparse.ArgumentParser(description='Valida um arquivo JSON contra o catálogo local.')
p.add_argument('file'); args=p.parse_args(); data=json.loads(Path(args.file).read_text(encoding='utf-8'))
errors=validate_episode(data)
if errors:
    print('JSON inválido:'); print('\n'.join('- '+e for e in errors)); sys.exit(1)
print('JSON válido: todos os IDs existem no manifest.json.')
