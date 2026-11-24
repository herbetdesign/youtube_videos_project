# Narração (TTS)

O projeto inclui um adaptador local opcional baseado em `pyttsx3`, que utiliza as vozes instaladas no sistema operacional. A qualidade depende das vozes disponíveis no Windows.

```powershell
python -m pip install -r requirements.txt
python audio/tts.py --episode examples/episode_001.json --output output/audio/narration.wav
```

Para listar vozes disponíveis, execute `python -c "import pyttsx3; e=pyttsx3.init(); print([(v.name,v.id) for v in e.getProperty('voices')])"`. Escolha uma voz em português do Brasil, se estiver instalada. Não há serviço de TTS em nuvem nesta configuração.
