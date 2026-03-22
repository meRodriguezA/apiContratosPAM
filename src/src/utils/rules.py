from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class FieldRule:
    excel_field: str
    required: bool = False
    validator: Optional[Callable[[str], bool]] = None
    error_message: str = "Valor inválido"
