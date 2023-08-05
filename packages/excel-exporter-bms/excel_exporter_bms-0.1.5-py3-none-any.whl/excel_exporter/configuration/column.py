from excel_exporter.configuration.cell_format import CellFormat
from excel_exporter.configuration.group import Group


class Column:
    def __init__(
        self,
        column_name: str,
        variable_name: str,
        cell_format: CellFormat,
        group: Group,
        column_width: int,
    ):
        self.column_name = column_name
        self.variable_name = variable_name
        self.cell_format = cell_format
        self.group = group
        self.column_width = column_width

    def __repr__(self):
        p = []
        p.append(f'column_name={self.column_name}')
        p.append(f'variable_name={self.variable_name}')
        p.append(f'cell_format={self.cell_format}')
        p.append(f'group={self.group}')
        p.append(f'column_width={self.column_width}')
        parameters = '\n'.join(p)
        return f'Column({parameters})'
