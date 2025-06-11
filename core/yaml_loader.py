import yaml

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if isinstance(data, list):
            return data

        elif isinstance(data, str):
            # Tenta dividir a string em linhas, se for um blob de texto
            lines = [line.strip() for line in data.splitlines() if line.strip()]
            return lines

        else:
            return []

    except Exception as e:
        print(f"Erro ao carregar YAML: {e}")
        return []
