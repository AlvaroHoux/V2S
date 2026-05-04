import os
import datetime

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