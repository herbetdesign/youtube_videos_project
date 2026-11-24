# Financial Animation Kit

Biblioteca inicial de personagens, cenários, objetos e motor SVG para produzir vídeos educativos sobre finanças, carreira, renda e negócios, no estilo cartoon 2D pastel inspirado na referência aprovada.

## O que vem neste repositório

- 5 personagens recorrentes com 10 expressões embutidas em SVG modular.
- 8 cenários vetoriais e 7 objetos reutilizáveis.
- Catálogo único em `manifest.json`.
- Motor de pré-visualização HTML/CSS/JavaScript.
- Gerador/validador JSON em Python, com integração opcional ao Ollama local.
- Adaptador opcional de narração offline com `pyttsx3`.
- Renderização de quadros com Playwright e codificação/mixagem com FFmpeg.
- Episódio demonstrativo e documentação para criação de novos episódios.

> **Estado:** versão inicial funcional para prototipagem. O desenho é uma biblioteca vetorial inicial; refine os assets e valide a qualidade de cada cena antes de produção em escala. O motor atualmente apresenta um personagem por cena, fundo, objetos, texto e movimentos básicos.

## Requisitos

- Python 3.10 ou superior.
- Ollama (opcional, apenas para converter storyboard em JSON).
- Chromium via Playwright para renderizar quadros.
- FFmpeg no PATH para gerar MP4.
- `pyttsx3` opcional para TTS usando uma voz instalada no sistema.

## Instalação no Windows

```powershell
py -3 -m venv .venv
.venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Instale FFmpeg e confirme que `ffmpeg -version` funciona no terminal. Para usar o Ollama, instale-o e baixe um modelo leve, por exemplo `ollama pull qwen2.5:3b`.

## Pré-visualizar o episódio de exemplo

Na raiz do repositório:

```powershell
python -m http.server 8000
```

Abra `http://localhost:8000/engine/?episode=../examples/episode_001.json`. O navegador precisa servir os arquivos por HTTP para permitir `fetch()` dos SVGs e do JSON.

## Validar JSON

```powershell
python python/validate_episode.py examples/episode_001.json
```

## Converter storyboard usando Ollama (opcional)

Crie um arquivo `storyboard.md` com o storyboard produzido pelo ChatGPT e execute:

```powershell
python python/scene_generator.py --storyboard storyboard.md --model qwen2.5:3b --output output/episode.json
```

Se o ChatGPT já entregar o JSON final, basta validar:

```powershell
python python/scene_generator.py --input examples/episode_001.json --output output/episode.json
```

## Gerar narração local (opcional)

```powershell
python audio/tts.py --episode examples/episode_001.json --output output/audio/narration.wav
```

A voz depende das vozes instaladas no Windows. Você também pode substituir esse arquivo por uma narração gravada ou gerada em outro serviço, respeitando as licenças e os termos aplicáveis.

## Gerar vídeo MP4

```powershell
python render/render_video.py --episode examples/episode_001.json --output output/episode-silent.mp4
python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.wav --output output/episode-final.mp4
```

O renderizador usa 12 FPS por padrão para reduzir o tempo de processamento em computadores modestos. É possível usar `--fps 15` ou `--fps 24`, sabendo que o número de quadros e o tempo de renderização aumentam.

## Como economizar tokens

1. Mantenha o `manifest.json` como catálogo oficial e envie esse arquivo ao ChatGPT, não todos os SVGs.
2. Peça ao ChatGPT para referenciar IDs existentes, sem redesenhar assets.
3. Gere apenas JSON de cenas para cada novo episódio.
4. Atualize os assets apenas quando houver uma melhoria visual reutilizável.

O repositório não elimina automaticamente tokens: o custo de contexto depende do conteúdo que for enviado ao modelo. A economia vem de reutilizar os arquivos e limitar o prompt ao catálogo e às instruções necessárias.

## Estrutura

```text
financial-animation-kit/
├── characters/       # Personagens e seus SVGs modulares
├── scenes/           # Cenários em SVG
├── objects/          # Objetos reutilizáveis em SVG
├── animations/       # Recursos e presets de animação
├── engine/           # Preview e motor SVG no navegador
├── python/           # Gerador e validador de cenas
├── audio/            # Integração TTS local
├── render/           # Renderização Playwright + FFmpeg
├── examples/         # Episódio demonstrativo
├── data/             # Schema JSON
├── docs/             # Guia visual, catálogo e workflow
└── manifest.json     # Índice central de recursos
```

## Contribuir com novos assets

- Use IDs em kebab-case.
- Preserve o estilo visual e os viewBoxes.
- Atualize `manifest.json` e `docs/asset-catalog.md`.
- Inclua uma cena de exemplo ou screenshot quando um novo recurso afetar o motor.
- Execute a validação JSON antes de enviar alterações.

## Licença

Código e assets SVG originais deste projeto são disponibilizados sob MIT. Consulte `LICENSE`.
