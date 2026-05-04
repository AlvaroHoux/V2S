import os
import sys
import re
from v2s.utils.ui import Spinner, print_success, print_error

# --- FUNÇÕES PARA SRT ---

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


# --- FUNÇÕES PARA ASS ---

def ass_time_to_ms(t):
    # Formato ASS: H:MM:SS.XX
    h, m, rest = t.split(':')
    s, cs = rest.split('.')
    # Converte centissegundos para milissegundos
    ms = int(cs.ljust(3, '0'))
    return int(h)*3600000 + int(m)*60000 + int(s)*1000 + ms

def ms_to_ass_time(ms):
    h = ms // 3600000
    ms %= 3600000
    m = ms // 60000
    ms %= 60000
    s = ms // 1000
    ms %= 1000
    cs = ms // 10  # ASS usa 2 dígitos para a fração
    return f"{h}:{m:02}:{s:02}.{cs:02}"

def fix_ass_by_word(input_file, output_file=None):
    with open(input_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    header_lines = []
    new_dialogues = []
    in_events = False
    format_order = []
    global_index = 0

    for line in lines:
        if not in_events:
            header_lines.append(line)
            if line.strip() == '[Events]':
                in_events = True
        else:
            if line.startswith('Format:'):
                header_lines.append(line)
                # Extrai a ordem das colunas, ex: Layer, Start, End, Style, Name, MarginL...
                format_order = [x.strip() for x in line[7:].split(',')]
            elif line.startswith('Dialogue:'):
                # Limita o split para não quebrar no meio do texto, que pode conter vírgulas
                parts = line[9:].split(',', len(format_order) - 1)
                if len(parts) < len(format_order):
                    continue
                
                start_idx = format_order.index('Start')
                end_idx = format_order.index('End')
                text_idx = format_order.index('Text')

                start_ms = ass_time_to_ms(parts[start_idx].strip())
                end_ms = ass_time_to_ms(parts[end_idx].strip())
                
                raw_text = parts[text_idx].strip()
                
                # Remove as tags de estilo do ASS (ex: {\an8}, {\c&HFFFFFF&}) antes de limpar
                clean_text = re.sub(r'\{.*?\}', '', raw_text)
                # Mantém seu filtro original
                clean_text = re.sub(r"[^\w\s]", "", clean_text)
                words = clean_text.split()
                
                if not words:
                    continue
                    
                duration = end_ms - start_ms
                step = duration / len(words)
                
                for i, word in enumerate(words):
                    w_start = start_ms + int(i * step)
                    w_end = start_ms + int((i + 1) * step)
                    
                    # Reconstrói a linha de diálogo mantendo o estilo original
                    new_parts = parts.copy()
                    new_parts[start_idx] = ms_to_ass_time(w_start)
                    new_parts[end_idx] = ms_to_ass_time(w_end)
                    new_parts[text_idx] = word + '\n' # Adiciona a quebra de linha removida no split
                    
                    new_dialogues.append('Dialogue: ' + ','.join(new_parts))
                    global_index += 1
            else:
                if line.strip():
                    header_lines.append(line)

    if output_file is None:
        output_file = input_file.replace('.ass', '_word.ass')

    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.writelines(header_lines)
        f.writelines(new_dialogues)

    return output_file, global_index


# --- CLI HANDLER ---

def cmd_split(args):
    entrada = args.input
    if not os.path.exists(entrada):
        print_error(f"File '{entrada}' not found!")
        sys.exit(1)

    _, ext = os.path.splitext(entrada)
    ext = ext.lower()

    if ext == '.srt':
        with Spinner("Splitting SRT by word..."):
            output_file, total = fix_srt_by_word(entrada, args.output)
        print_success(f"SRT split by word saved to: \033[1m{output_file}\033[0m ({total} words)")
        
    elif ext == '.ass':
        with Spinner("Splitting ASS by word..."):
            output_file, total = fix_ass_by_word(entrada, args.output)
        print_success(f"ASS split by word saved to: \033[1m{output_file}\033[0m ({total} words)")
        
    else:
        print_error(f"Unsupported file format: {ext}. Only .srt and .ass are supported.")
        sys.exit(1)

    return output_file