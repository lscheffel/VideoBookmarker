import os
from typing import List

def export_playlist_to_m3u(urls: List[str], filepath: str) -> bool:
    """
    Exporta uma lista de URLs para um arquivo .m3u.
    
    Cada URL é colocada em uma linha separada no arquivo.
    Retorna True se exportação ocorrer com sucesso, False caso contrário.
    """
    try:
        # Garante que a extensão seja .m3u
        if not filepath.lower().endswith(".m3u"):
            filepath += ".m3u"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")  # Cabeçalho padrão m3u
            for url in urls:
                f.write(f"{url}\n")
        return True
    except Exception as e:
        print(f"Erro ao exportar playlist para m3u: {e}")
        return False
