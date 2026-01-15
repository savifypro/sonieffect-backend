import subprocess
from pathlib import Path
import shutil
import re
import random
import os
from typing import Optional, Callable, Dict

from core import SERVER_URL
from dir_config import AUDIO_DIR, VIDEO_DIR

LOGO_PATH = Path("assets/logo/logo.png").resolve()

def save_uploaded_file(upload_file) -> str:
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', upload_file.filename)
    target_path = VIDEO_DIR / safe_name
    with open(target_path, "wb") as f:
        shutil.copyfileobj(upload_file.file, f)
    return str(target_path)

def convert_video_to_audio(
    input_path: str,
    out_format: str = "mp3",
    bitrate: str = "192k",
    progress_callback: Optional[Callable[[int], None]] = None
) -> str:
    input_file = Path(input_path).resolve()
    if not input_file.exists() or not str(input_file).startswith(str(VIDEO_DIR.resolve())):
        raise ValueError("Security Violation: Invalid Input Path")

    rand_3 = random.randint(100, 999)
    stem = re.sub(r'[^a-zA-Z0-9_-]', '_', input_file.stem)
    output_filename = f"SoniEffect_Converted_{stem}.{out_format}"
    out_path = AUDIO_DIR / output_filename
    
    has_logo = LOGO_PATH.exists()

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "info",
        "-hwaccel", "auto",
        "-thread_queue_size", "4096",
        "-i", str(input_file)
    ]

    if has_logo:
        cmd.extend(["-i", str(LOGO_PATH)])

    cmd.extend(["-map", "0:a:0"])
    
    if has_logo:
        cmd.extend(["-map", "1:v:0", "-disposition:v:0", "attached_pic"])

    if out_format == "mp3":
        cmd.extend([
            "-c:a", "libmp3lame", "-b:a", bitrate,
            "-compression_level", "0",
            "-id3v2_version", "3",
            "-metadata:s:v", "title=Album cover",
            "-metadata:s:v", "comment=Cover (front)"
        ])
    elif out_format == "m4a":
        cmd.extend(["-c:a", "aac", "-b:a", bitrate, "-cutoff", "20000"])
    else:
        cmd.extend(["-c:a", "flac" if out_format == "flac" else "pcm_s16le"])

    cmd.extend([
        "-metadata", f"title=SoniEffect Audio #{rand_3}",
        "-metadata", "artist=SoniEffect",
        "-metadata", "album=SoniEffect Conversions",
        "-movflags", "+faststart",
        "-threads", "0",
        str(out_path)
    ])

    process = subprocess.Popen(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        text=True, bufsize=1, encoding='utf-8'
    )

    duration = 0.0
    pattern_dur = re.compile(r"Duration:\s(\d+):(\d+):(\d+\.\d+)")
    pattern_time = re.compile(r"time=(\d+):(\d+):(\d+\.\d+)")

    while True:
        line = process.stderr.readline()
        if not line: break
        
        if duration <= 0:
            match = pattern_dur.search(line)
            if match:
                h, m, s = map(float, match.groups())
                duration = h * 3600 + m * 60 + s
        else:
            if progress_callback:
                t_match = pattern_time.search(line)
                if t_match:
                    h, m, s = map(float, t_match.groups())
                    curr = h * 3600 + m * 60 + s
                    progress_callback(min(int((curr / duration) * 100), 100))

    process.wait()
    
    if input_file.exists():
        os.remove(input_file)

    return str(out_path)

def delete_file(filename: str) -> bool:
    try:
        safe_name = Path(filename).name
        target = (AUDIO_DIR / safe_name).resolve()
        if target.exists() and str(target).startswith(str(AUDIO_DIR.resolve())):
            target.unlink()
            return True
        return False
    except:
        return False