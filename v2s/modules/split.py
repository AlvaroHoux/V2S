import os
import sys
import re
from v2s.utils.ui import Spinner, print_success, print_error

def srt_time_to_ms(t):
    h, m, rest = t.split(':')
    s, ms = rest.split(',')
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + int(ms)

def ms_to_srt_time(ms):
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def fix_srt_by_word(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    new_blocks = []
    global_index = 1

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        
        match = re.match(r'(\S+)\s*-->\s*(\S+)', lines[1])
        if not match:
            continue
            
        start_ms = srt_time_to_ms(match.group(1))
        end_ms = srt_time_to_ms(match.group(2))

        raw_text = ' '.join(line.strip() for line in lines[2:] if line.strip())
        clean_text = re.sub(r"[^\w\s]", "", raw_text)
        words = clean_text.split()
        
        if not words:
            continue

        duration = end_ms - start_ms
        step = duration / len(words)
        
        for i, word in enumerate(words):
            w_start = start_ms + int(i * step)
            w_end = start_ms + int((i + 1) * step)
            new_blocks.append(
                f"{global_index}\n{ms_to_srt_time(w_start)} --> {ms_to_srt_time(w_end)}\n{word}"
            )
            global_index += 1

    if output_file is None:
        output_file = input_file.replace('.srt', '_word.srt')

    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write('\n\n'.join(new_blocks) + '\n\n')

    return output_file, global_index - 1

def cmd_split(args):
    entrada = args.input
    if not os.path.exists(entrada):
        print_error(f"File '{entrada}' not found!")
        sys.exit(1)

    with Spinner("Splitting SRT by word..."):
        output_file, total = fix_srt_by_word(entrada, args.output)

    print_success(f"SRT split by word saved to: \033[1m{output_file}\033[0m ({total} words)")
    return output_file