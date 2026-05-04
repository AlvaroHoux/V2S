import os
import sys
import re
from v2s.utils.ui import print_success, print_error, Spinner, print_info
from v2s.modules.transcribe import cmd_transcribe

def srt_time_to_ass(time_str):
    # SRT time: HH:MM:SS,mmm -> ASS time: H:MM:SS.cs
    h, m, s_ms = time_str.split(':')
    s, ms = s_ms.split(',')
    
    h = str(int(h)) # single digit hours
    cs = ms[:2] # centiseconds
    return f"{h}:{m}:{s}.{cs}"

def convert_srt_to_ass(srt_path, ass_path):
    with open(srt_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        
    blocks = re.split(r'\n\n+', content.strip())
    
    ass_header = """[Script Info]
Title: V2S Generated ASS
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_events = []
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', lines[1])
            if time_match:
                start = srt_time_to_ass(time_match.group(1))
                end = srt_time_to_ass(time_match.group(2))
                text = '\\N'.join(lines[2:])
                ass_events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
                
    with open(ass_path, 'w', encoding='utf-8-sig') as f:
        f.write(ass_header + '\n'.join(ass_events) + '\n')

def cmd_ass(args):
    entrada = args.input
    if not os.path.exists(entrada):
        print_error(f"File '{entrada}' not found!")
        sys.exit(1)

    pasta = args.output_dir or "output"
    os.makedirs(pasta, exist_ok=True)
    
    srt_path = entrada
    
    # If not an SRT file, generate it first using the transcribe module
    if not entrada.lower().endswith('.srt'):
        print_info(f"Input is not an SRT file. Generating SRT first...")
        srt_path = cmd_transcribe(args)

    with Spinner("Converting to ASS format..."):
        base = os.path.splitext(os.path.basename(srt_path))[0]
        ass_path = os.path.join(pasta, base + ".ass")
        convert_srt_to_ass(srt_path, ass_path)

    print_success(f"ASS generated at: \033[1m{ass_path}\033[0m")
    return ass_path
