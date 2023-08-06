from sap2000.log import Log
import comtypes.client
from sys import exit
from sap2000.Base.constants import SapDefinitions
from sap2000.Base import units
import pandas as pd
from rich.progress import Progress

sapconstants = SapDefinitions()

class Sap:
    log = Log()
    log.setLevel(10)

    # Constructor
    def __init__(self):
        log = self.log
        log.info("SAP2000 python script has been initiated.")        
    
        #attach to a running instance of SAP2000
        self.mySapObject, self.SapModel = attach_to_existing_SAP_instance()

        #Initialize Attributes
        self.Base = None
        return
    
    def analyze(self, cases_to_run:list=[], exclude_cases:list=[], all_cases: bool=True):
        """
        This function runs an analysis on a given set of load cases using the SAP2000 API.

        The function takes three arguments:

            self: an instance of the object that this function belongs to
            cases_to_run: a list of strings representing the names of the load cases to run in the analysis (default is an empty list)
            exclude_cases: a list of strings representing the names of the load cases to exclude from the analysis (default is an empty list)
            all_cases: a boolean value indicating whether to run all defined load cases in the model (default is True)

        The function first sets the run flags for the specified load cases to run and exclude. If the all_cases argument is set to True, the function sets the run flag for all defined load cases in the model to be run in the analysis. The function then runs the analysis using the SAP2000 API and returns the status of the analysis.
        """
        SapModel = self.SapModel
        log = self.log
        
        with Progress(transient=True) as progress:
            progress.add_task('Setting up loadcases to run', total=None)

            #Include cases to run
            [SapModel.Analyze.SetRunCaseFlag(case, True) for case in cases_to_run]

            #Exclude cases to run
            [SapModel.Analyze.SetRunCaseFlag(case, False) for case in exclude_cases]

            #Set all cases to be run
            if all_cases:
                df = self.get_case_status()
                [SapModel.Analyze.SetRunCaseFlag(case, True) for case in df.Case.values]

        with Progress(transient=True) as progress:
            progress.add_task('Running Analysis', total=None)
            #Run Analysis
            ret = self.SapModel.Analyze.RunAnalysis()
            
        self.log.debug("Model Analysis Run")
        return ret

    def save_model(self, savepath:str =None):
        """Saves SAP model to the `savepath`, if no save path is provided, saves to the default path

        Args:
            savepath (str, optional): Filepath to where the model needs to be saved. Defaults to None.
        """
        if savepath:
            ret = self.SapModel.File.Save(savepath)
        else:
            ret = self.SapModel.File.Save()
        self.log.debug("Model Saved")
        return ret
    
    def  get_case_status(self)-> pd.DataFrame:
        """
        This function returns a Pandas DataFrame containing the status of all defined load cases in a SAP2000 model.

        The function takes a self argument, which is an instance of the object that this function belongs to. The function returns a DataFrame with three columns: 'Case', 'Run_Flag', and 'Current_Status'. The 'Case' column contains the names of the load cases, the 'Run_Flag' column contains a boolean value indicating whether the load case is set to run in an analysis, and the 'Current_Status' column contains a string indicating the current status of the load case.

        The function retrieves the case status and run flags using the SAP2000 API and then creates the DataFrame using this information. The 'Current_Status' column is mapped to string values for easier interpretation.
        """
        _, case_name, current_status, command_status = self.SapModel.Analyze.GetCaseStatus()
        if command_status != 0:
            self.log.error('Some error happened. Command `Analyze.GetCaseStatus()` failed.')
            return pd.DataFrame()

        _, _, run_flag, command_status = self.SapModel.Analyze.GetRunCaseFlag()
        if command_status != 0:
            self.log.error('Some error happened. Command `Analyze.GetRunCaseFlag()` failed.')
            return pd.DataFrame()

        
        df = pd.DataFrame({'Case': case_name, 'Run_Flag': run_flag, 'Current_Status':current_status})

        df.Current_Status = df.Current_Status.map({1:'Not run', 2:'Could not start', 3:'Not finished', 4:'Finished'})

        return df


    def __str__(self) -> str:
        return f"Instance of `SapClass`"

    def __repr__(self) -> str:
        return f"SapClass()"

    def __del__(self):
        #close Sap2000
        ret = self.mySapObject.ApplicationExit(False)
        self.SapModel = None
        self.mySapObject = None

    def add_loadcombination(self, combo_name: str, combo_type:str):
        """Create a load combination and set the combination type

        Args:
            combo_name (str): Name of the combination
            combo_type (str): Type of combination, accepts: [Linear Additive, Envelope, Absolute Additive, SRSS, Range Additive]

        Returns:
            int : 0-Success
        """

        combo_type_map = {
            "Linear Additive": 0, "Envelope":1, "Absolute Additive": 2, "SRSS": 3, "Range Additive": 4
        }
        if not combo_type in combo_type_map.keys():
            self.log.error(f"\"{combo_type}\" is not an acceptable input for `combo_type`. Acceptable inputs include: {', '.join(list(combo_type_map.keys()))}")
            return -1
        return self.SapModel.RespCombo.Add(combo_name, combo_type_map[combo_type])

    def add_to_loadcombo(self, base_combo_name: str, adding_case_name: str, factor: float, adding_combo:bool = False):
        """Adds the load case/combo to the base combo name. If adding one combo inside another, be sure to set `adding_combo` to True

        Args:
            base_combo_name (str): The combo to add to  
            adding_case_name (str): The case or combo being added
            factor (float): load case factor
            adding_combo (bool, optional): Set to True if `adding_case_name` is a combo. Defaults to False.

        Returns:
            int : 0-Success
        """
        return self.SapModel.RespCombo.SetCaseList(base_combo_name, int(adding_combo), adding_case_name, factor)

    def lock(self):
        """Lock the Analysis model
        """
        if not self.SapModel.GetModelIsLocked():
            self.SapModel.SetModelIsLocked(True)

    def unlock(self):
        """Unlock the analysis model
        """
        if self.SapModel.GetModelIsLocked():
            self.SapModel.SetModelIsLocked(False)

def attach_to_existing_SAP_instance() -> tuple[comtypes.POINTER, comtypes.POINTER]:
    """Creates a comtype instance and returns the SAPObject and SAPModel attached to the existing instance
    """
    try:
        #get the active SapObject
        sapobject = comtypes.client.GetActiveObject("CSI.SAP2000.API.SapObject")
        sapmodel = sapobject.SapModel
        print("Attached to existing instance")
        return sapobject, sapmodel

    except (OSError, comtypes.COMError):
        print("No running instance of the program found or failed to attach.")
        exit(-1)