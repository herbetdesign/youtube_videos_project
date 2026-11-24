# Workflow

1. ChatGPT cria roteiro, narração e storyboard.
2. Envie ao ChatGPT `manifest.json` e `data/episode.schema.json`.
3. Peça JSON com IDs já existentes; não redesenhe os recursos em cada episódio.
4. Valide com `python python/validate_episode.py caminho-do-episodio.json`.
5. Pré-visualize usando `python -m http.server 8000` e a página em `/engine/`.
6. Gere voz no ElevenLabs ou Google AI Studio e salve MP3/WAV em `output/audio/`.
7. Renderize o vídeo silencioso com Playwright + FFmpeg.
8. Combine narração e música opcional com `render/assemble_video.py`.
