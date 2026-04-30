from v2s.utils.ui import print_step, print_info
from v2s.modules.tts import cmd_tts
from v2s.modules.srt import cmd_srt
from v2s.modules.split import cmd_split

def cmd_all(args):
    print_step("Passo 1/3 — Gerando áudio TTS")
    audio_path = cmd_tts(args)

    print_step("Passo 2/3 — Transcrevendo com Whisper")
    args.input = audio_path
    args.output_dir = args.output_dir or "output"
    srt_path = cmd_srt(args)

    print_step("Passo 3/3 — Separando SRT por palavra")
    args.input = srt_path
    args.output = None
    cmd_split(args)

    print_info("Fluxo completo finalizado!")