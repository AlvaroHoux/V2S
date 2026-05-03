import os
import sys
from datetime import datetime
from v2s.utils.ui import Spinner, print_success
from v2s.utils.voice import select_voice

def aplicar_patch_pytorch():
    import torch
    _original_load = torch.load
    torch.load = lambda *args, **kwargs: _original_load(*args, **{**kwargs, 'weights_only': False})

def configurar_caminho_saida(nome_saida_fornecido, pasta="output", ext=".wav"):
    os.makedirs(pasta, exist_ok=True)
    if nome_saida_fornecido:
        if not nome_saida_fornecido.lower().endswith(ext):
            nome_saida_fornecido += ext
        return os.path.join(pasta, nome_saida_fornecido)
    return os.path.join(pasta, datetime.now().strftime("%d-%m-%y.%H-%M-%S") + ext)

def cmd_tts(args):
    import torch
    from TTS.api import TTS

    caminho_final = configurar_caminho_saida(args.output)
    idioma = args.language or "en"
    voz_ref = select_voice(args.voice)

    with Spinner("Starting XTTSv2 and loading model..."):
        aplicar_patch_pytorch()
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    
    print_success("XTTSv2 model loaded!")

    with Spinner("Cloning voice and generating audio..."):
        tts.tts_to_file(
            text=args.text,
            speaker_wav=voz_ref,
            language=idioma,
            file_path=caminho_final
        )
    
    print_success(f"Audio saved to: \033[1m{caminho_final}\033[0m")
    return caminho_final