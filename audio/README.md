# Áudio e narração

## Fluxo recomendado: ElevenLabs ou Google AI Studio

Gere a voz no serviço de sua preferência e baixe como MP3 ou WAV. Use o mesmo texto de narração do roteiro e salve, por exemplo, em:

```text
output/audio/narration.mp3
```

Depois combine ao vídeo silencioso:

```powershell
python render/assemble_video.py --video output/episode-silent.mp4 --voice output/audio/narration.mp3 --output output/episode-final.mp4
```

O FFmpeg aceita MP3, WAV e outros formatos comuns. Não é necessário TTS local quando você já tem a narração do ElevenLabs ou Google AI.

## Alternativa local opcional

O `tts.py` usa `pyttsx3` e vozes instaladas no Windows. A qualidade depende das vozes do sistema; para a voz final do canal, prefira o ElevenLabs ou Google AI Studio.
