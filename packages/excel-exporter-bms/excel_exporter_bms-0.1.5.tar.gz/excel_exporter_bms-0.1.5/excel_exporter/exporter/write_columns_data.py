from typing import Dict, List

from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from excel_exporter.configuration.column import Column as ColumnConfiguration
from excel_exporter.configuration.cell_format import CellFormat


def write_columns_data(
    ws: Worksheet,
    ws_data: Dict[str, List],
    columns_config: Dict[str, ColumnConfiguration],
    start_col: int = 2,
):
    # print(ws_data.keys())
    for col_number, col_config in enumerate(
        columns_config.values(), start=start_col
    ):
        col_data = ws_data[col_config.variable_name]
        format = col_config.cell_format
        write_column(ws, col_number, col_data, format)


def write_column(
    ws: Worksheet,
    col_number: int,
    col_data: List,
    format: CellFormat,
    start_row: int = 4,
):
    alignment = Alignment(
        horizontal=format.horizontal_alignment,
        vertical=format.vertical_alignment,
        wrap_text=format.line_break,
    )
    font = Font(size=format.font_size)
    url_font = Font(size=format.font_size, underline='single', color='0563C1')
    for row_number, value in enumerate(col_data, start=start_row):
        if isinstance(value, list) or isinstance(value, tuple):
            value, url = value[0], value[1]
        else:
            url = None
        cell = ws.cell(row=row_number, column=col_number)
        cell.value = value
        cell.alignment = alignment
        if not url:
            cell.font = font
        else:
            cell.hyperlink = url
            cell.font = url_font
