import sys
import argparse
from v2s.utils.ui import print_banner, print_error
from v2s.modules.tts import cmd_tts
from v2s.modules.style_tts import cmd_styletts2
from v2s.modules.srt import cmd_srt
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

    p_srt = subparsers.add_parser("srt")
    p_srt.add_argument("input")
    p_srt.add_argument("-m", "--model", default="base")
    p_srt.add_argument("-l", "--language", default="en")
    p_srt.add_argument("-d", "--output-dir", default="output", dest="output_dir")
    p_srt.set_defaults(func=cmd_srt)

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
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n")
        print_error("Cancelado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print("\n")
        print_error(f"Erro inesperado: {e}")
        sys.exit(1)