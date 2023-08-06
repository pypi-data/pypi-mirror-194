from openpyxl.cell.cell import Cell, ILLEGAL_CHARACTERS_RE
from openpyxl.utils.exceptions import IllegalCharacterError


def robust_write_cell(cell, value):
    try:
        cell.value = value
    except IllegalCharacterError as e:
        print(f'Found illegal characters on attempt to write on {str(cell)}')
        clean_value = ILLEGAL_CHARACTERS_RE.sub(r'', value)
        illegal_chars = ILLEGAL_CHARACTERS_RE.findall(value)
        illegal_chars = ' '.join(
            '0x' + f'{ord(c):02x}'.upper() for c in set(illegal_chars)
        )
        cell.value = clean_value
        print(f'  - Illegal characters: {illegal_chars}')
        print(f'  - The value was cleaned and written to cell: {clean_value}')
