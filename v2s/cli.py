import os
import sys
import argparse
import warnings

# Suppress specific FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*_register_pytree_node.*")

# Suppress NLTK downloads prints
try:
    import nltk
    _original_download = nltk.download
    def _quiet_download(*args, **kwargs):
        kwargs['quiet'] = True
        return _original_download(*args, **kwargs)
    nltk.download = _quiet_download
except ImportError:
    pass

from v2s.utils.ui import print_banner, print_error
from v2s.modules.tts.xtts import cmd_tts
from v2s.modules.tts.style_tts import cmd_styletts2
from v2s.modules.transcribe import cmd_transcribe
from v2s.modules.ass import cmd_ass
from v2s.modules.split import cmd_split
from v2s.modules.pipeline import cmd_all

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog="v2s",
        description="V2S — Voice & Subtitle Toolkit",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_tts = subparsers.add_parser("tts")
    p_tts.add_argument("text")
    p_tts.add_argument("-o", "--output", default=None)
    p_tts.add_argument("-v", "--voice", default=None)
    p_tts.add_argument("-l", "--language", default="en")
    p_tts.add_argument("-e", "--engine", choices=["xtts", "styletts2"], default="styletts2")
    
    def route_tts(args):
        if args.engine == "styletts2":
            return cmd_styletts2(args)
        return cmd_tts(args)
        
    p_tts.set_defaults(func=route_tts)

    p_transcribe = subparsers.add_parser("transcribe")
    p_transcribe.add_argument("input")
    p_transcribe.add_argument("-m", "--model", default="base")
    p_transcribe.add_argument("-l", "--language", default="en")
    p_transcribe.add_argument("-d", "--output-dir", default="output", dest="output_dir")
    p_transcribe.set_defaults(func=cmd_transcribe)

    p_ass = subparsers.add_parser("ass")
    p_ass.add_argument("input")
    p_ass.add_argument("-m", "--model", default="base")
    p_ass.add_argument("-l", "--language", default="en")
    p_ass.add_argument("-d", "--output-dir", default="output", dest="output_dir")
    # Novo argumento para o efeito na legenda
    p_ass.add_argument("--effect", default=None, help="Subtitle effect. Use predefined names (e.g., 'pop', 'fade') or a custom ASS tag string.")
    p_ass.set_defaults(func=cmd_ass)

    p_split = subparsers.add_parser("split")
    p_split.add_argument("input")
    p_split.add_argument("-o", "--output", default=None)
    p_split.set_defaults(func=cmd_split)

    p_all = subparsers.add_parser("all")
    p_all.add_argument("text")
    p_all.add_argument("-o", "--output", default=None)
    p_all.add_argument("-v", "--voice", default=None)
    p_all.add_argument("-l", "--language", default="en")
    p_all.add_argument("-m", "--model", default="base")
    p_all.add_argument("-d", "--output-dir", default="output", dest="output_dir")
    p_all.add_argument("-e", "--engine", choices=["xtts", "styletts2"], default="xtts")
    p_all.add_argument("-f", "--format", choices=["srt", "ass"], default="ass", help="Subtitle format (srt without effects, ass with effects)")
    # O mesmo argumento na pipeline completa
    p_all.add_argument("--effect", default=None, help="Subtitle effect. Use predefined names (e.g., 'pop', 'fade') or a custom ASS tag string.")
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n")
        print_error("Cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print("\n")
        print_error(f"Unexpected error: {e}")
        sys.exit(1)