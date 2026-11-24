#!/usr/bin/env python3
"""Render a scene JSON to a silent MP4 using the local SVG engine + Playwright + FFmpeg."""
import argparse, json, shutil, subprocess, sys, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
ROOT=Path(__file__).resolve().parents[1]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--episode',default=str(ROOT/'examples'/'episode_001.json'));p.add_argument('--output',default=str(ROOT/'output'/'episode-silent.mp4'));p.add_argument('--fps',type=int,default=12);p.add_argument('--width',type=int,default=1920);p.add_argument('--height',type=int,default=1080);p.add_argument('--keep-frames',action='store_true');a=p.parse_args()
    try: from playwright.sync_api import sync_playwright
    except ImportError: raise SystemExit('Instale Playwright: pip install playwright && playwright install chromium')
    ep=Path(a.episode).resolve(); data=json.loads(ep.read_text(encoding='utf-8'))
    from sys import path as syspath; syspath.insert(0,str(ROOT/'python')); from scene_generator import validate_episode
    errors=validate_episode(data)
    if errors: raise SystemExit('JSON inválido:\n'+'\n'.join(errors))
    duration=sum(float(s['duration_seconds']) for s in data['scenes']); fps=max(1,min(a.fps,30)); total=round(duration*fps)
    frame_dir=ROOT/'output'/'frames'; frame_dir.mkdir(parents=True,exist_ok=True)
    for old in frame_dir.glob('frame_*.png'): old.unlink()
    handler=partial(QuietHandler,directory=str(ROOT)); server=ThreadingHTTPServer(('127.0.0.1',0),handler); threading.Thread(target=server.serve_forever,daemon=True).start(); port=server.server_address[1]
    episode_rel=ep.relative_to(ROOT).as_posix(); url=f'http://127.0.0.1:{port}/engine/index.html?episode=../{episode_rel}'
    print(f'Renderizando {duration:.1f}s em {fps} fps ({total} frames).')
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True); page=browser.new_page(viewport={'width':a.width,'height':a.height},device_scale_factor=1)
            page.goto(url,wait_until='networkidle',timeout=120000); page.wait_for_function('window.engineReady===true',timeout=120000)
            page.add_style_tag(content=f'main{{max-width:none!important;margin:0!important;padding:0!important}}#stage-wrap{{width:{a.width}px!important;height:{a.height}px!important;aspect-ratio:auto!important}}#stage{{width:{a.width}px!important;height:{a.height}px!important}}.toolbar,.timeline,.hint{{display:none!important}}')
            stage=page.locator('#stage')
            for i in range(total):
                t=i/fps; page.evaluate('(t)=>window.renderAt(t)',t)
                page.wait_for_timeout(35)
                stage.screenshot(path=str(frame_dir/f'frame_{i:06d}.png'),animations='disabled')
                if i%100==0 or i==total-1: print(f'  {i+1}/{total} frames')
            browser.close()
    finally: server.shutdown()
    out=Path(a.output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg: raise SystemExit('FFmpeg não encontrado no PATH. Instale FFmpeg e tente novamente.')
    cmd=[ffmpeg,'-y','-framerate',str(fps),'-i',str(frame_dir/'frame_%06d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','21','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True);print(f'Vídeo sem áudio salvo em: {out}')
    if not a.keep_frames: shutil.rmtree(frame_dir,ignore_errors=True)
if __name__=='__main__': main()
