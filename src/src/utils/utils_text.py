import re
import unicodedata


def remove_accents(text: str) -> str:
    text = str(text).strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text


def normalize(text: str) -> str:
    return remove_accents(text).lower().strip()


def is_blank(text: str) -> bool:
    return not str(text).strip()


def safe_filename(text: str) -> str:
    """
    Limpia un texto para usar como carpeta/archivo en Windows.
    Quita tildes y elimina caracteres no permitidos.
    """
    text = remove_accents(text).strip()

    # Caracteres ilegales en Windows: \ / : * ? " < > |
    text = re.sub(r'[\\/:*?"<>|]', "", text)

    # Colapsar espacios
    text = re.sub(r"\s+", " ", text)

    return text
