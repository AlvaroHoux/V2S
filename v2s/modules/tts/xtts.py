from datetime import datetime
from v2s.utils.ui import Spinner, print_success
from v2s.utils.voice import select_voice
from v2s.modules.tts import configurar_caminho_saida, aplicar_patch_pytorch

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