from src.integrations.google_sheets_client import GoogleSheetsConnector
from src.utils.utils_text import normalize
from src.integrations.sheet_to_word_mapper import header_to_variable
from src.utils.console_table_printer import print_excel_word_table


class SpreadsheetDataReader:
    def __init__(self, credentials_json_path: str, debug_table: bool = True):
        self.conn = GoogleSheetsConnector(credentials_json_path)
        self.debug_table = debug_table

    def _build_contexts(self, headers: list[str], row_values: list[str]):
        context_word = {}
        context_excel = {}

        for h, v in zip(headers, row_values):
            context_excel[h] = v
            key = header_to_variable(h)
            if key:
                context_word[key] = v

        return context_word, context_excel

    def _debug_print(self, context_excel: dict):
        if self.debug_table:
            print_excel_word_table(context_excel)

    def get_context_by_animal(self, spreadsheet_name: str, animal_input: str):
        sheet = self.conn.open_by_name(spreadsheet_name)
        ws = sheet.sheet1

        headers = ws.row_values(1)
        animals_col = ws.col_values(2)

        search = normalize(animal_input)

        for row_index, cell_value in enumerate(animals_col[2:], start=2):
            if normalize(cell_value) == search:
                row_values = ws.row_values(row_index)
                context_word, context_excel = self._build_contexts(headers, row_values)
                self._debug_print(context_excel)
                return context_word, context_excel

        raise ValueError(f"No se encontró el animal: {animal_input}")

    def get_context_by_sheet_row(self, spreadsheet_name: str, sheet_row_number: int):
        sheet = self.conn.open_by_name(spreadsheet_name)
        ws = sheet.sheet1

        if sheet_row_number < 2:
            raise ValueError("La fila 1 es la cabecera. Introduce una fila >= 2.")

        headers = ws.row_values(1)
        row_values = ws.row_values(sheet_row_number)

        if not row_values:
            raise ValueError(f"La fila {sheet_row_number} no existe o está vacía.")

        context_word, context_excel = self._build_contexts(headers, row_values)
        self._debug_print(context_excel)
        return context_word, context_excel
