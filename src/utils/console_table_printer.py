from src.integrations.sheet_to_word_mapper import header_to_variable


def _format_value(value) -> str:
    if value is None:
        return "(VACÍO)"
    value = str(value).strip()
    return value if value else "(VACÍO)"


def print_excel_word_table(context_excel: dict):
    if not context_excel:
        print("\n[INFO] No hay datos para mostrar.\n")
        return

    headers = list(context_excel.keys())
    values = [_format_value(v) for v in context_excel.values()]
    vars_word = [f"{{{{{header_to_variable(h)}}}}}" for h in headers]

    max_header = max(len(h) for h in headers)
    max_value = max(len(v) for v in values)
    max_var = max(len(vw) for vw in vars_word)

    line = "─" * (max_header + max_value + max_var + 12)

    print("\nDatos detectados (Excel → Word)")
    print(line)
    print(
        f"{'COLUMNA EXCEL'.ljust(max_header)}  |  "
        f"{'VALOR'.ljust(max_value)}  |  "
        f"{'VARIABLE DOCUMENTO'.ljust(max_var)}"
    )
    print(line)

    for h, v, vw in zip(headers, values, vars_word):
        print(
            f"{h.ljust(max_header)}  |  "
            f"{v.ljust(max_value)}  |  "
            f"{vw.ljust(max_var)}"
        )

    print(line)
    print("")
