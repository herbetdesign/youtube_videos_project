# Fluxo de produção

1. **ChatGPT:** escreva roteiro e storyboard com narração, tempos e ações.
2. **Catálogo:** utilize apenas IDs presentes em `manifest.json`.
3. **JSON de episódio:** estruture cenas conforme `data/episode.schema.json`.
4. **Validação:** execute `python python/validate_episode.py examples/episode_001.json`.
5. **Ollama (opcional):** salve o storyboard em .md e execute `python python/scene_generator.py --storyboard storyboard.md --model qwen2.5:3b`.
6. **Preview:** rode `python -m http.server 8000` na raiz e abra `http://localhost:8000/engine/?episode=../examples/episode_001.json`.
7. **Narração local:** gere `output/audio/narration.wav` usando `audio/tts.py` ou coloque uma narração gravada no mesmo caminho.
8. **Render silencioso:** `python render/render_video.py --episode examples/episode_001.json`.
9. **Finalização:** `python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.wav`.
10. **Revisão:** confira pronúncia, sincronização, direitos dos assets, números financeiros e legendas antes de publicar.

Os scripts de renderização capturam quadros individualmente com Chromium via Playwright e usam FFmpeg para codificar. O tempo de renderização depende da CPU, da duração, do FPS e da complexidade das cenas.
