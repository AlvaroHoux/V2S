from v2s.utils.ui import print_step, print_info
from v2s.modules.tts import cmd_tts
from v2s.modules.style_tts import cmd_styletts2
from v2s.modules.srt import cmd_srt
from v2s.modules.split import cmd_split

def cmd_all(args):
    print_step(f"Step 1/3 — Generating TTS audio ({args.engine.upper()})")
    
    if args.engine == "styletts2":
        audio_path = cmd_styletts2(args)
    else:
        audio_path = cmd_tts(args)

    print_step("Step 2/3 — Transcribing with Whisper")
    args.input = audio_path
    args.output_dir = args.output_dir or "output"
    srt_path = cmd_srt(args)

    print_step("Step 3/3 — Splitting SRT by word")
    args.input = srt_path
    args.output = None
    cmd_split(args)

    print_info("Complete workflow finished!")