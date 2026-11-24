# Financial Animation Kit — 2D Blocky

Fábrica de vídeos educativos com avatares 2D blocados, inspirados na linguagem visual de jogos de personagens: cabeças quadradas, troncos retangulares, membros articulados, contornos grossos e cores vivas. Os personagens e cenários são originais e não usam marcas ou assets oficiais de jogos.

## Biblioteca incluída

- 8 personagens recorrentes: Herbert, Mentora, Investidor, Amigo, Especialista, Empreendedora, Tech/IA e Briqueiro.
- SVGs modulares com cabeça, tronco, braços e pernas separados por grupos articulados.
- 10 expressões faciais e 11 movimentos básicos.
- 10 cenários, 12 objetos, 6 roupas e 5 acessórios.
- Manifesto central `manifest.json` e schema JSON.
- Motor HTML/CSS/JavaScript, geração opcional de cenas via Ollama, Playwright e FFmpeg.
- Narração externa MP3/WAV de ElevenLabs ou Google AI Studio.

## Instalação Windows

```powershell
py -3 -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

Instale FFmpeg e confirme `ffmpeg -version`.

## Validar e visualizar

```powershell
python python/validate_episode.py examples/episode_001.json
python -m http.server 8000
```

Abra `http://localhost:8000/engine/?episode=../examples/episode_001.json`.

## Renderizar com áudio externo

Salve sua narração MP3/WAV em `output/audio/narration.mp3`:

```powershell
python render/render_video.py --episode examples/episode_001.json --output output/episode-silent.mp4 --fps 12
python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.mp3 --output output/episode-final.mp4
```

`episode-silent.mp4` é intermediário; `episode-final.mp4` é o arquivo com narração.

## Trocar roupa e acessórios em uma cena

```json
{"character":"investor","outfit":"business-suit","accessories":["tie-red","glasses"]}
```

Consulte os IDs existentes em `manifest.json`. Para economizar tokens, envie ao ChatGPT somente o manifesto, o schema e o briefing, não todos os SVGs.

## Pastas principais

`characters/`, `scenes/`, `objects/`, `outfits/`, `accessories/`, `animations/`, `engine/`, `python/`, `render/`, `examples/`.

Código e assets vetoriais originais sob licença MIT.
