import os
import sys
from datetime import datetime
from v2s.utils.ui import Spinner, print_success, print_error, print_info

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
    voz_ref = args.voice or "voz_referencia.mp3"
    idioma  = args.language or "en"

    if not os.path.exists(voz_ref):
        print_error(f"Arquivo de referência '{voz_ref}' não encontrado!")
        print_info("Use --voice para apontar para o arquivo de referência correto.")
        sys.exit(1)

    with Spinner("Iniciando XTTSv2 e carregando modelo..."):
        aplicar_patch_pytorch()
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
    
    print_success("Modelo XTTSv2 carregado!")

    with Spinner("Clonando voz e gerando áudio..."):
        tts.tts_to_file(
            text=args.text,
            speaker_wav=voz_ref,
            language=idioma,
            file_path=caminho_final
        )
    
    print_success(f"Áudio salvo em: \033[1m{caminho_final}\033[0m")
    return caminho_final