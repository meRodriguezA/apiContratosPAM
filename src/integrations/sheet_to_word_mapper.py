import re
from src.utils.utils_text import remove_accents


def header_to_variable(header: str) -> str:
    """
    Convierte cabecera de Excel/Sheet en variable para Word (docxtpl).
    Ejemplos:
      - "NombreAnimal" -> "nombreAnimal"
      - "Nombre Representante PAM" -> "nombreRepresentantePam"
      - "Fecha_Adopcion" -> "fechaAdopcion"
    """
    header = remove_accents(header).strip()

    header = re.sub(r"([a-z])([A-Z])", r"\1 \2", header)
    header = header.replace("_", " ").replace("-", " ")

    parts = header.split()
    if not parts:
        return ""

    first = parts[0].lower()
    rest = [p.capitalize() for p in parts[1:]]
    return first + "".join(rest)
