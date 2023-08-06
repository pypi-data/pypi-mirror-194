import pandas as pd
import comtypes
from IPython.display import display, HTML

class Table:
    def __init__(self, sapclass):
        self.sapclass = sapclass
    
    def __str__(self) -> str:
        f"Table procedures"
    
    def __repr__(self) -> str:
        f"Table(sapclass=\"{self.sapclass}\")"
    
    @property
    def available(self) -> list:
        "Returns a list of available tables"
        return self.sapclass.SapModel.DatabaseTables.GetAvailableTables()[1]

    @property
    def all(self) -> list:
        "Returns a list of all tables in SAP"
        return self.sapclass.SapModel.DatabaseTables.GetAllTables()

    def col_description(self, table_name: str) -> pd.DataFrame:
        """Returns a dataframe of the table columns, units used and description

        Args:
            table_name (str): Name of the table
        """
        if self._is_available(table_name=table_name):
            table = self.sapclass.SapModel.DatabaseTables.GetAllFieldsInTable(table_name)
        
            return pd.DataFrame({
                'key': table[2],
                'name' : table[3],
                'description': table[4],
                'units': table[5],
                'isimportable': table[6]
            }).set_index('key')
        
    def get(self, table_name: str) -> pd.DataFrame:
        """Returns the dataframe form of the specified table

        Args:
            table_name (str): Name of table, see Tables.available for list of options
        """
        if self._is_available(table_name=table_name):
            table = self.sapclass.SapModel.DatabaseTables.GetTableForDisplayArray(
                table_name, GroupName="", FieldKeyList=""
                )

            return _build_dataframe_from_array(column_list=table[2], item_list=table[4])
        else:
            return pd.DataFrame()
        
    def display_to_jupyter(self, table_name: str) -> None:
        "Displays the specified table to a jupyter display"
        table_df = self.get(table_name=table_name)
        display(HTML(table_df.to_html()))
    
    def _is_available(self, table_name: str) -> bool:
        "Checks if the specified name is in available table names"
        if not table_name in self.available:
            print(f"Requested table(`{table_name}`) not in the list of Available tables")
            print(f"Use `Tables.available` to see the list of available tables")
            return False
        return True

def _build_dataframe_from_array(column_list: list[str], item_list: list) -> pd.DataFrame:
    """Returns the dataframe form of the specified array

    Args:
        column_list (list[str]): List of column names
        table_name (list): Array of items to go inside table

    Returns:
        pd.DataFrame: Dataframe version of the table
    """
    num_cols = len(column_list)
    data = [item_list[x: x+num_cols] for x in range(0, len(item_list), num_cols)]
    return pd.DataFrame(data, columns = column_list)