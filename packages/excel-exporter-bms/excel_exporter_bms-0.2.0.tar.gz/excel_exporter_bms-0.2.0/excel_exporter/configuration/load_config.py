from typing import Dict
import yaml


from excel_exporter.configuration.are_strings_grouped import (
    are_strings_grouped,
)
from excel_exporter.configuration.cell_format import CellFormat
from excel_exporter.configuration.column import Column
from excel_exporter.configuration.excel_configuration import ExcelConfiguration
from excel_exporter.configuration.group import Group
from excel_exporter.configuration.sheet import Sheet


def parse_yaml(yaml_data: Dict) -> ExcelConfiguration:
    # 1. File name
    file_name = yaml_data['file_name']
    update_message = str(yaml_data['update_message']).strip()
    # 2. Cell Formats
    cell_formats = {}
    for cell_format_data in yaml_data['cell_formats']:
        cell_format = CellFormat(
            cell_format_data['format_name'],
            cell_format_data['font_size'],
            cell_format_data['horizontal_alignment'],
            cell_format_data['vertical_alignment'],
            cell_format_data['line_break'],
        )
        cell_formats[cell_format.format_name] = cell_format
    # 3. Sheets
    sheets = {}
    for sheet_data in yaml_data['sheets']:
        # 3,1. In each sheet, groups
        groups = {}
        for group_data in sheet_data['groups']:
            group = Group(
                group_data['group_name'], group_data['background_color']
            )
            groups[group.group_name] = group
        # 3.2 In each sheet, columns
        columns = {}
        for col_data in sheet_data['columns']:
            # Each column references to a previously loaded cell formart
            cell_format = cell_formats.get(col_data['cell_format'], None)
            if not cell_format:
                raise ValueError(
                    f"Cell format {col_data['cell_format']} not found"
                )
            # Each column references to a previously loaded group
            group = groups.get(col_data['group'], None)
            if not group:
                raise ValueError(f"Group {col_data['group']} not found")
            # Finish creating the column
            column = Column(
                col_data['column_name'],
                col_data['variable_name'],
                cell_format,
                group,
                col_data['column_width'],
            )
            columns[column.column_name] = column
        # Verify if columns are really grouped
        cols_groups = [col.group.group_name for col in columns.values()]
        if not are_strings_grouped(cols_groups):
            raise ValueError(f'Columns are not grouped: \n{cols_groups}')
        # Update date reference to a previously load cell format
        update_date_format = cell_formats.get(
            sheet_data['update_date_format'], None
        )
        if not update_date_format:
            raise ValueError(
                f"Cell format {sheet_data['update_date_format']} not found"
            )
        # Finish creating the sheet
        sheet = Sheet(
            sheet_data['sheet_name'], update_date_format, groups, columns
        )
        sheets[sheet_data['sheet_name']] = sheet
    # Finish creating the configuration
    return ExcelConfiguration(file_name, update_message, cell_formats, sheets)


def load_config(file_path: str, encoding: str = 'utf8') -> ExcelConfiguration:
    with open(file_path, 'r', encoding=encoding) as file:
        yaml_data = yaml.safe_load(file)
    return parse_yaml(yaml_data)
