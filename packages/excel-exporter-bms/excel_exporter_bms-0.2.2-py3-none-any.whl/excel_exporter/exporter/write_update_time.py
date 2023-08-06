from datetime import datetime

from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from excel_exporter.configuration.cell_format import CellFormat
from excel_exporter.exporter.character_validation import robust_write_cell


def write_update_time(
    ws: Worksheet,
    update_time: datetime,
    format: CellFormat,
    message: str,
):
    cell = ws.cell(row=1, column=2)
    # Write update time
    full_update_time_message = f'{message} {update_time.strftime("%Y-%m-%d")}'
    robust_write_cell(cell, full_update_time_message)
    # Format update time cell
    alignment = Alignment(
        horizontal=format.horizontal_alignment,
        vertical=format.vertical_alignment,
        wrap_text=format.line_break,
    )
    font = Font(size=format.font_size)
    cell.alignment = alignment
    cell.font = font
