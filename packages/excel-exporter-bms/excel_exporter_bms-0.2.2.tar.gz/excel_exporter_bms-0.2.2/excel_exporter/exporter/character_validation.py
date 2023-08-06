from openpyxl.cell.cell import Cell, ILLEGAL_CHARACTERS_RE
from openpyxl.utils.exceptions import IllegalCharacterError


def clean_string(string):
    return ILLEGAL_CHARACTERS_RE.sub(r'', string)


def find_illegal_chars(string):
    illegal_chars = ILLEGAL_CHARACTERS_RE.findall(string)
    illegal_chars = [f'{ord(c):02x}'.upper() for c in set(illegal_chars)]
    illegal_chars = [f'0x{c}' for c in illegal_chars]
    return ' '.join(illegal_chars)


def robust_write_cell(cell, value):
    try:
        cell.value = value
    except IllegalCharacterError as e:
        print(f'Found illegal characters on attempt to write on {str(cell)}')
        clean_value = clean_string(value)
        illegal_chars = find_illegal_chars(value)
        cell.value = clean_value
        print(f'  - Illegal characters: {illegal_chars}')
        print(f'  - The value was cleaned and written to cell: {clean_value}')
