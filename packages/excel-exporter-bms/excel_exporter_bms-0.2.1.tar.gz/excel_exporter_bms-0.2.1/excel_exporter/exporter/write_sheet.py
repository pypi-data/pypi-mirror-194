from datetime import datetime
from typing import Dict, List

from openpyxl.worksheet.worksheet import Worksheet

from excel_exporter.configuration.sheet import Sheet as SheetConfiguration
from excel_exporter.exporter.apply_sheet_configs import apply_sheet_configs
from excel_exporter.exporter.write_groups_header import write_groups_header
from excel_exporter.exporter.write_update_time import write_update_time
from excel_exporter.exporter.write_columns_data import write_columns_data
from excel_exporter.exporter.write_columns_header import write_columns_header


def write_sheet(
    ws: Worksheet,
    ws_data: Dict[str, List],
    ws_config: SheetConfiguration,
    update_time: datetime,
    update_message: str,
):
    # Sheet name
    ws.title = ws_config.sheet_name
    write_update_time(
        ws, update_time, ws_config.update_date_format, update_message
    )
    write_groups_header(ws, ws_config.groups, ws_config.groups_limits())
    write_columns_header(ws, ws_config.columns)
    write_columns_data(ws, ws_data, ws_config.columns)
    apply_sheet_configs(ws, ws_config)
