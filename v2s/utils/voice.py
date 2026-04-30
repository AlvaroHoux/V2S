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
        print_error(f"Nenhum arquivo de áudio encontrado na pasta '{voices_dir}'!")
        print_info("Adicione um arquivo de referência e tente novamente.")
        sys.exit(1)

    if voice_arg:
        match = next((v for v in voices if v.lower() == voice_arg.lower() or v.startswith(voice_arg)), None)
        if match:
            return os.path.join(voices_dir, match)
        print_error(f"Voz '{voice_arg}' não encontrada em '{voices_dir}'.")
        sys.exit(1)

    print("\n\033[1;94m🎙️ Vozes disponíveis em 'voices/':\033[0m")
    for v in voices:
        print(f"  - {v}")

    default_voice = voices[0]
    escolha = input(f"\nDigite o nome da voz (ou Enter para \033[1m{default_voice}\033[0m): ").strip()

    if not escolha:
        selecionada = default_voice
    else:
        selecionada = next((v for v in voices if v.lower().startswith(escolha.lower())), default_voice)
        if selecionada == default_voice and escolha.lower() not in default_voice.lower():
            print_error(f"Voz '{escolha}' não encontrada. Usando padrão.")

    print_success(f"Voz selecionada: {selecionada}\n")
    return os.path.join(voices_dir, selecionada)