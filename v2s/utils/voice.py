import os
import sys
from v2s.utils.ui import print_error, print_info, print_success

def select_voice(voice_arg=None, voices_dir="voices"):
    if voice_arg and os.path.exists(voice_arg):
        return voice_arg

    os.makedirs(voices_dir, exist_ok=True)
    valid_exts = ('.mp3', '.wav', '.flac', '.m4a', '.ogg')
    voices = sorted([f for f in os.listdir(voices_dir) if f.lower().endswith(valid_exts)])

    if not voices:
        print_error(f"No audio files found in directory '{voices_dir}'!")
        print_info("Add a reference audio file and try again.")
        sys.exit(1)

    if voice_arg:
        match = next((v for v in voices if v.lower() == voice_arg.lower() or v.startswith(voice_arg)), None)
        if match:
            return os.path.join(voices_dir, match)
        print_error(f"Voice '{voice_arg}' not found in '{voices_dir}'.")
        sys.exit(1)

    abs_voices_dir = os.path.abspath(voices_dir)
    print(f"\n\033[1;94m🎙️ Available voices:\033[0m")
    print(f"  \033[90m(Retrieved from {abs_voices_dir})\033[0m")
    
    for i, v in enumerate(voices, 1):
        print(f"  {i}. {v}")

    default_voice = voices[0]
    escolha = input(f"\nEnter the voice number (or Enter for \033[1m1 - {default_voice}\033[0m): ").strip()

    if not escolha:
        selecionada = default_voice
    elif escolha.isdigit() and 1 <= int(escolha) <= len(voices):
        selecionada = voices[int(escolha) - 1]
    else:
        selecionada = next((v for v in voices if v.lower().startswith(escolha.lower())), default_voice)
        if selecionada == default_voice and escolha.lower() not in default_voice.lower():
            print_error(f"Voice '{escolha}' not found. Using default.")

    print_success(f"Selected voice: {selecionada}\n")
    return os.path.join(voices_dir, selecionada)
