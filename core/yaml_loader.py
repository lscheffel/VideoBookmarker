import os
from typing import List

def load_urls_from_file(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        return []

    urls = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and line.startswith("http"):
                urls.append(line)
    return urls
