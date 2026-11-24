# Workflow

1. ChatGPT cria roteiro/storyboard.
2. Envie `manifest.json` e `data/episode.schema.json` para usar IDs existentes.
3. Salve JSON e valide usando `python python/validate_episode.py arquivo.json`.
4. Pré-visualize por `python -m http.server 8000` e abra o engine.
5. Gere narração no ElevenLabs ou Google AI Studio em MP3/WAV.
6. Renderize vídeo com Playwright + FFmpeg.
7. Combine áudio externo usando `render/assemble_video.py`.
