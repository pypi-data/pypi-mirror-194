from rich.console import Console
from rich.theme import Theme
import pandas as pd

custom_theme = Theme({'success': 'green', 'error': 'bold red'})
console = Console(theme=custom_theme)

class Results:
    def __init__(self, sapclass):
        self.sapclass = sapclass
        self.results = self.sapclass.SapModel.Results
    
    def __str__(self) -> str:
        f"Typical Routines class"
    
    def __repr__(self) -> str:
        f"Results(sapclass=\"{self.sapclass}\")"

    def select_for_output_cases(self, case_list: list[str]):
        for case in case_list:
            self.results.Setup.SetCaseSelectedForOutput(case)

    def select_for_output_all_cases(self):
        self.select_for_output_case(case_list=list(self.sapclass.get_case_status().Case))
    
    def select_for_output_combos(self, combo_list: list[str]):
        for combo in combo_list:
            self.results.Setup.SetComboSelectedForOutput(combo)

    def select_for_output_all_combos(self):
        self.select_for_output_combos(combo_list=list(self.sapclass.SapModel.RespCombo.GetNameList()[1]))
    
    def deselect_all_case_and_combo(self):
        self.results.Setup.DeselectAllCasesAndCombosForOutput()

    def get_beam_design_forces(self, beam_name: str) -> pd.DataFrame:
        """Returns the beam design forces for the specified beam name"""
        table = self.sapclass.SapModel.DesignResults.DesignForces.BeamDesignForces(beam_name)

        df = pd.DataFrame({ 'framename': table[1], 'comboname': table[2], 'station':table[3],
            'P':table[4], 'V2': table[5], 'V3': table[6], 'T': table[7], 'M2': table[8],
            'M3': table[9] })
        df['comboname'] = df['comboname'].astype('category')
        force_unit, distance_unit, _ = self.sapclass.Units.get()
        df['P'] = df['P'] * force_unit
        df['V2'] = df['V2'] * force_unit
        df['V3'] = df['V3'] * force_unit
        df['T'] = df['T'] * force_unit * distance_unit
        df['M2'] = df['M2'] * force_unit * distance_unit
        df['M3'] = df['M3'] * force_unit * distance_unit

        return get_min_max(df, columns=['P', 'V2', 'V3', 'T', 'M2', 'M3'], ref_column=['comboname', 'station'])


def _get_min_max_of_single_column(df: pd.DataFrame, column: str, ref_column:list[str]) -> pd.DataFrame:
    """Returns a multi-index df containing the `min`, `max`, `abs_min`, `abs_max` for the specified column
    along with the corresponding values of the `ref_column` columns

    Args:
        df (pd.DataFrame): dataframe to lookup values in
        column (str): Name of the column
        ref_column (list): List of reference columns to return. (sim to VLOOKUP)

    Returns:
        pd.DataFrame: Multi-Index df containing `min`, `max`, `abs_min`, `abs_max` for the specified column
    """
    columns = [column]
    columns.extend(ref_column)
    sorted_df = df.sort_values(columns, ascending=True)
    min_row = sorted_df.iloc[0]
    max_row = sorted_df.iloc[-1]
    min_value = min_row[columns]
    max_value = max_row[columns]
    min_df = min_value.rename({column:'value'}).rename('min')
    max_df = max_value.rename({column:'value'}).rename('max')

    abs_df = df.copy()
    abs_df[column] = abs(df[column])
    sorted_abs_df = abs_df.sort_values(columns, ascending=True)
    abs_min_row = sorted_abs_df.iloc[0]
    abs_max_row = sorted_abs_df.iloc[-1]
    abs_min_value = abs_min_row[columns]
    abs_max_value = abs_max_row[columns]
    abs_min_df = abs_min_value.rename({column:'value'}).rename('absmin')
    abs_max_df = abs_max_value.rename({column:'value'}).rename('absmax')

    df = pd.concat([min_df, max_df, abs_min_df, abs_max_df], axis=1).transpose()
    df['column'] = column
    df = (
        df
        .reset_index(level=0)
        .set_index(['column', 'index'])

    )
    return df

def get_min_max(df: pd.DataFrame, columns: list[str], ref_column:list) -> pd.DataFrame:
    """Runs the `._get_min_max_of_single_column` function over multiple columns, 
    concats the results and returns

    Args:
        df (pd.DataFrame): dataframe to lookup values in
        column (str): list of name of the columns
        ref_column (list): List of reference columns to return. (sim to VLOOKUP)

    Returns:
        pd.DataFrame: Multi-Index df containing `min`, `max`, `abs_min`, `abs_max` for the specified columns
    """
    rows = [_get_min_max_of_single_column(df, column, ref_column) for column in columns]
    return pd.concat(rows)