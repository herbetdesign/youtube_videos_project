# Financial Animation Kit — 2D Blocky

Kit de vídeos financeiros com avatares 2D blocados originais, membros articulados, contornos pretos e cores vivas, inspirado na linguagem visual de jogos de avatar (sem logos ou personagens oficiais).

## Biblioteca

- 8 personagens: Herbert, Mentora, Investidor, Amigo, Especialista, Empreendedora, Tech/IA e Briqueiro.
- 10 expressões faciais e 11 movimentos.
- 10 cenários, 12 objetos, 6 roupas e 5 acessórios.
- Motor SVG/HTML/CSS/JavaScript, gerador JSON opcional com Ollama, Playwright e FFmpeg.
- Narração MP3/WAV de ElevenLabs ou Google AI Studio.

## Instalação Windows

```powershell
py -3 -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```
Confirme `ffmpeg -version`.

## Ver o elenco

Depois de atualizar o repositório, abra `docs/character-roster.html` no navegador para ver os oito avatares lado a lado.

## Validar e pré-visualizar

```powershell
python python/validate_episode.py examples/episode_001.json
python -m http.server 8000
```

Abra `http://localhost:8000/engine/?episode=../examples/episode_001.json`.

## Renderizar com narração externa

Coloque MP3/WAV em `output/audio/narration.mp3` e rode:

```powershell
python render/render_video.py --episode examples/episode_001.json --output output/episode-silent.mp4 --fps 12
python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.mp3 --output output/episode-final.mp4
```

## Roupa/acessórios por cena

O JSON aceita `outfit` e `accessories`; os SVGs usam `data-part` para anexar as peças aos grupos articulados, acompanhando os movimentos. Consulte `manifest.json` para IDs.

## Pastas

`characters/`, `scenes/`, `objects/`, `outfits/`, `accessories/`, `animations/`, `engine/`, `python/`, `render/`, `examples/`.

Para economizar tokens, forneça ao ChatGPT apenas manifesto, schema e briefing. Código e SVGs originais sob MIT.
