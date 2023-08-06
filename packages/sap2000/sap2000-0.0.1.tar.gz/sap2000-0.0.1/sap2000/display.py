from rich import print
from rich.table import Table

def generate_table(header_row:list, values:list[list], title:str="") -> Table:
    """Make a new table."""
    table = Table(title=title)
    for item in header_row:
        table.add_column(str(item))

    if values:
        for row in values:
            table.add_row(**row)
    return table