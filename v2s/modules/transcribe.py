import os
import sys
import subprocess
from v2s.utils.ui import Spinner, print_success, print_error, print_info

def cmd_transcribe(args):
    entrada = args.input
    if not os.path.exists(entrada):
        print_error(f"File '{entrada}' not found!")
        sys.exit(1)

    model = args.model or "base"
    language = args.language or "en"
    pasta = args.output_dir or "output"
    os.makedirs(pasta, exist_ok=True)

    cmd = [
        "whisper", entrada,
        "--model", model,
        "--language", language,
        "--output_format", "srt",
        "--word_timestamps", "True",
        "--output_dir", pasta,
    ]

    print_info(f"Running: {' '.join(cmd)}")

    with Spinner("Transcribing with Whisper..."):
        result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print_error("Whisper returned an error:")
        print(result.stderr)
        sys.exit(1)

    base = os.path.splitext(os.path.basename(entrada))[0]
    srt_path = os.path.join(pasta, base + ".srt")

    print_success(f"SRT generated at: \033[1m{srt_path}\033[0m")
    return srt_path