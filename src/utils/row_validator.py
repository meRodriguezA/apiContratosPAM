from src.utils.utils_text import is_blank
from src.utils.rules import FieldRule


class SpreadsheetRowValidator:
    def __init__(self, rules: list[FieldRule]):
        self.rules = rules

    def validate(self, context_excel: dict) -> list[str]:
        errors = []

        for rule in self.rules:
            value = context_excel.get(rule.excel_field, "")

            if rule.required and is_blank(value):
                errors.append(f"Campo obligatorio vacío: '{rule.excel_field}'")
                continue

            if is_blank(value):
                continue

            if rule.validator and not rule.validator(str(value).strip()):
                errors.append(
                    f"'{rule.excel_field}': {rule.error_message} (valor: '{value}')"
                )

        return errors
