import os
import sys
import nltk
from styletts2 import tts as stts2
from v2s.utils.ui import Spinner, print_success
from v2s.utils.voice import select_voice
from v2s.modules.tts import configurar_caminho_saida, aplicar_patch_pytorch

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

def cmd_styletts2(args):
    caminho_final = configurar_caminho_saida(args.output)
    voz_ref = select_voice(args.voice)

    with Spinner("Carregando modelo StyleTTS2..."):
        aplicar_patch_pytorch()
        styletts = stts2.StyleTTS2()
    
    print_success("Modelo StyleTTS2 carregado!")

    with Spinner("Clonando voz e gerando áudio com StyleTTS2..."):
        styletts.inference(
            text=args.text,
            target_voice_path=voz_ref,
            output_wav_file=caminho_final
        )
    
    print_success(f"Áudio salvo em: \033[1m{caminho_final}\033[0m")
    return caminho_final