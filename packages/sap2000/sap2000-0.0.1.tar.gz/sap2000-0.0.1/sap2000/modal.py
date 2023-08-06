import pandas as pd
from rich.console import Console
from rich.theme import Theme
from sap2000.display import generate_table
from rich.live import Live

custom_theme = Theme({'success': 'green', 'error': 'bold red'})
console = Console(theme=custom_theme)

class ModalAnalysis:
    def __init__(self, sapclass, log):
        self.sapclass = sapclass
        self.log = log
    
    def __str__(self) -> str:
        f"Modal analysis procedures"
    
    def __repr__(self) -> str:
        f"ModalAnalysis(sapclass=\"{self.sapclass}\", log=\"{self.log}\")"

    def capture_95pct_mass(self) -> int:
        """
        This function performs an iterative analysis to determine the minimum number of modes required for a given load case in order to achieve 95% participation in modal mass for the X, Y, and Z directions.

        The function returns an integer representing the minimum number of modes required for the specified load case to achieve 95% modal mass participation.

        The function performs the analysis by first setting the number of modes for the MODAL load case and then running the model with the given number of modes. The function then checks the modal mass participation ratio and if it is at least 0.95 for all three directions, the function returns the number of modes used in the analysis. If the ratio is not at least 0.95 for all three directions, the function increments the number of modes and repeats the analysis until the ratio is satisfied. The progress of the analysis is displayed in a live table that updates after each iteration.
        """
        num_modes = 5
        header_row = ["Iteration", "Number of Modes", "Ux", "Uy", "Uz", "Status"]
        table_rows = []
        
        title="Iterative analysis to find out min. num of modes for 95% modal mass paticipation"

        
        cases_df = self.get_case_status()
        exclusion_case = list(cases_df.Case)
        exclusion_case.remove('MODAL')

        iteration = 1
        with Live(generate_table(header_row=header_row, values=table_rows, title=title), refresh_per_second=4) as live:
            while True:
                assert self.SapModel.LoadCases.ModalEigen.SetNumberModes("MODAL", num_modes, num_modes) ==0
                self.analyze(cases_to_run=['MODAL'], exclude_cases=exclusion_case)
                df = self.getinfo()
                ratio = self._check_modalmassparticipation(df, suppress_output=True)
                if ratio['Ux'] >=0.95 and ratio['Uy'] >=0.95 and ratio['Uz'] >=0.95:
                    table_rows.append([
                        f"{iteration}", f"{num_modes}", 
                        f"[{'green' if ratio['Ux'] >=0.95 else 'red'}]{ratio['Ux']:.2f}",
                        f"[{'green' if ratio['Uy'] >=0.95 else 'red'}]{ratio['Uy']:.2f}", 
                        f"[{'green' if ratio['Uz'] >=0.95 else 'red'}]{ratio['Uz']:.2f}", 
                        "[green]Satisfied"
                    ])
                    live.update(generate_table(header_row=header_row, values=table_rows, title=title))
                    break
                else:
                    table_rows.append([f"{iteration}", f"{num_modes}", 
                        f"[{'green' if ratio['Ux'] >=0.95 else 'red'}]{ratio['Ux']:.2f}",
                        f"[{'green' if ratio['Uy'] >=0.95 else 'red'}]{ratio['Uy']:.2f}", 
                        f"[{'green' if ratio['Uz'] >=0.95 else 'red'}]{ratio['Uz']:.2f}", 
                        "[red]Not Satisfied"])
                    live.update(generate_table(header_row=header_row, values=table_rows, title=title))

                num_modes += 1
                iteration += 1
        
        return num_modes

    def getinfo(self) -> pd.DataFrame:
        """
        This function returns a Pandas DataFrame containing the modal participating mass ratios for the MODAL load case in a SAP2000 model.

        The function takes a self argument, which is an instance of the object that this function belongs to. The function returns a DataFrame with four columns: 'Period', 'Ux', 'Uy', and 'Uz'. The 'Period' column contains the periods of the modes, the 'Ux' column contains the modal participating mass ratios for the X direction, the 'Uy' column contains the modal participating mass ratios for the Y direction, and the 'Uz' column contains the modal participating mass ratios for the Z direction.

        The function first checks if the MODAL load case has been run and if not, runs the case using the SAP2000 API. The function then retrieves the modal participating mass ratios using the SAP2000 API and creates the DataFrame using this information.
        """
        sap = self.sapclass
        df = sap.get_case_status()
        if df.loc[df.Case == "MODAL","Current_Status"].iloc[0] != "Finished":
            sap.analyze(cases_to_run=['MODAL'])

        _, _, _, _, period, ux, uy, uz, *_ , command_status = sap.mySapObject.SapModel.Results.ModalParticipatingMassRatios()
        if command_status != 0:
            self.log.error('Some error happened. Command `Results.ModalPeriod()` failed.')
            return pd.DataFrame()
        df = pd.DataFrame({'Period':period, 'Ux':ux, 'Uy': uy, 'Uz': uz})
        return df

    def _check_modalmassparticipation(df: pd.DataFrame, suppress_output:bool=False) -> dict:
        """Function to check if the modal mass participation exceeds 95% requirement as set out by code. Returns a dict of mass participation ratio.

        Args:
            dataframe (pd.DataFrame): Pandas dataframe containing timeperiod and modal mass participation factors for each modal case
        """
        Ux = df.Ux.sum()
        Uy = df.Uy.sum()
        Uz = df.Uz.sum()
        if not suppress_output:
            console.print(f"UX: {Ux:.2f} | {'Acceptable' if Ux >= 0.95 else 'Threshold not met'}", style=f"{'success' if Ux >= 0.95 else 'error'}")
            console.print(f"UY: {Uy:.2f} | {'Acceptable' if Uy >= 0.95 else 'Threshold not met'}", style=f"{'success' if Uy >= 0.95 else 'error'}")
            console.print(f"UZ: {Uz:.2f} | {'Acceptable' if Uz >= 0.95 else 'Threshold not met'}", style=f"{'success' if Uz >= 0.95 else 'error'}")
        return {"Ux": Ux, "Uy": Uy, "Uz":Uz}


    def check_massparticipation(self):
        """Function to check if the modal mass participation exceeds 95% requirement as set out by code.
        """
        df = self.getinfo()
        self._check_modalmassparticipation(df)