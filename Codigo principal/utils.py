import unicodedata

def normalize(text: str) -> str:
    """Elimina acentos y convierte a minúsculas."""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()