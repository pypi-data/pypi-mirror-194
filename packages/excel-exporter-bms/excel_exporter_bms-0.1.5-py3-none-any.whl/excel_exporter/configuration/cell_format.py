class CellFormat:
    def __init__(
        self,
        format_name: str,
        font_size: int,
        horizontal_alignment: str,
        vertical_alignment: str,
        line_break: bool,
    ):
        self.format_name = format_name
        self.font_size = font_size
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment
        self.line_break = line_break

    def __repr__(self):
        p = []
        p.append(f'format_name={self.format_name}')
        p.append(f'font_size={self.font_size}')
        p.append(f'horizontal_alignment={self.horizontal_alignment}')
        p.append(f'vertical_alignment={self.vertical_alignment}')
        p.append(f'line_break={self.line_break}')
        parameters = ', '.join(p)
        return f'CellFormat({parameters})'
