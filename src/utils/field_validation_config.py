from src.utils.rules import FieldRule
from src.core.validators import is_date_dd_mm_yyyy


VALIDATION_RULES = [
    FieldRule("Nombre Animal", required=True, error_message="Debe estar relleno"),
    FieldRule("Nombre Representante PAM", required=True, error_message="Debe estar relleno"),
    FieldRule(
        "Fecha Adopcion",
        required=True,
        validator=is_date_dd_mm_yyyy,
        error_message="Formato inválido. Debe ser dd/MM/yyyy",
    ),
]
