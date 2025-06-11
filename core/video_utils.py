import requests
from typing import Optional
from bs4 import BeautifulSoup
import os
import re
from html import unescape

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def validate_url(url: str, timeout: int = 5) -> bool:
    """
    Verifica se a URL está acessível (status 200).
    """
    try:
        response = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_video_title(url: str, timeout: int = 7) -> Optional[str]:
    """
    Faz o scraping simples do título da página do vídeo.
    Retorna None se não conseguir obter.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Tenta pegar a tag <title>
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.text.strip()
            # Limpeza básica, retirar o nome do site (exemplo " - Xvideos.com")
            if " - " in title:
                title = title.split(" - ")[0].strip()
            return title
        return None
    except Exception:
        return None

def download_video(url: str, output_folder: str, filename: Optional[str] = None) -> Optional[str]:
    """
    Baixa o vídeo da URL para a pasta especificada.
    Retorna o caminho completo do arquivo baixado ou None em caso de falha.
    Observação: funciona se o link permite download direto.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if not filename:
            filename = url.split("/")[-1].split("?")[0]
            if not filename:
                filename = "video.mp4"
        
        filepath = os.path.join(output_folder, filename)

        with requests.get(url, headers=HEADERS, stream=True) as r:
            r.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        return filepath
    except Exception as e:
        print(f"Erro no download do vídeo: {e}")
        return None

def get_video_info(page_url):
    """Retorna o título e o link do vídeo .mp4 a partir da página do Xvideos"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(page_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None

        html = resp.text
        title_match = re.search(r"setVideoTitle\('(.+?)'\);", html)
        high_match = re.search(r"setVideoUrlHigh\('(.+?)'\);", html)

        title = unescape(title_match.group(1)) if title_match else None
        high_url = high_match.group(1) if high_match else None

        return {
            "title": title,
            "high": high_url
        } if high_url else None

    except Exception as e:
        print("Erro no scraping de vídeo:", e)
        return None