@echo off
cd /d "%~dp0.."
py python/validate_episode.py examples/episode_001.json
pause
