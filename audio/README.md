# Áudio e narração

## Fluxo recomendado: ElevenLabs ou Google AI Studio

Gere a voz no serviço de sua preferência e baixe o áudio como MP3 ou WAV. Use o texto de narração do JSON para evitar diferenças em relação ao roteiro. Salve o arquivo, por exemplo, em:

```text
output/audio/narration.mp3
```

Depois combine-o ao vídeo renderizado:

```powershell
python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.mp3 --output output/episode-final.mp4
```

O parâmetro `--voice` aceita um caminho para um formato de áudio suportado pelo FFmpeg, incluindo MP3 e WAV. Não é necessário instalar TTS local quando a narração já vem pronta do ElevenLabs ou Google AI Studio.

## Alternativa opcional: voz local

O auxiliar `tts.py` usa `pyttsx3` e as vozes instaladas no sistema. A qualidade depende das vozes disponíveis no Windows; não é o caminho recomendado para a voz final do canal.

```powershell
pip install pyttsx3
python audio/tts.py --episode examples/episode_001.json --output output/audio/narration.wav
```

Para listar as vozes instaladas:

```powershell
python -c "import pyttsx3; e=pyttsx3.init(); print([(v.name,v.id) for v in e.getProperty('voices')])"
```

Revise pronúncia, pausas e tempo do áudio antes de finalizar o episódio.
