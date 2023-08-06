import pandas as pd
from rich.console import Console
from rich.theme import Theme
from sap2000.display import generate_table
from rich.live import Live
from sap2000.Base.constants import REBARS

from sap2000.user_interact import (
    _ui_get_seismic_parameters)


custom_theme = Theme({'success': 'green', 'error': 'bold red'})
console = Console(theme=custom_theme)


class Routines:
    def __init__(self, sapclass, log):
        self.sapclass = sapclass
        self.log = log
    
    def __str__(self) -> str:
        f"Typical Routines class"
    
    def __repr__(self) -> str:
        f"Routines(sapclass=\"{self.sapclass}\", log=\"{self.log}\")"

    def setup_template(self, rebars:bool=True, concrete:bool=True):
        """Routine to set default parameters and setting for AK files

        Args:
            rebars (bool, optional): Removes unused rebars and adds all Canadian rebars. Defaults to True.
            concrete (bool, optional): Creates concrete material properties per CSA A23.3. Defaults to True.
        """
        current_units = self.sapclass.SapModel.GetPresentUnits()

        if rebars:
            self.Materials.template_rebar_setup()
        if concrete:
            self.Materials.template_conc_material_setup()

        #Set the unit back to original
        self.sapclass.change_units(unit_type_int=current_units)

    def setup_response_spectrum_analysis(self):
        """Sets up the basic functions, cases and combinations for a response spectrum analysis. 
        It creates a response spectrum function and two response spectrum load cases for the x and y directions, and then creates a load combination called 'SPECXY' of type 'SRSS' that combines the two response spectrum load cases with a factor of 1 for each. 
        Finally, it sets a note for the 'SPECXY' load combination indicating that the user should run the analysis and adjust the factor to scale the base shear to 80%/100% of the static procedure.
        """
        rs = self.sapclass.ResponseSpectrum
        func = rs.create_function()
        p = _ui_get_seismic_parameters()
        specx = rs.create_loadcase(1, func, p.Rd, p.Ro, p.Ie)
        specy = rs.create_loadcase(2, func, p.Rd, p.Ro, p.Ie)

        self.sapclass.add_loadcombination('SPECXY', 'SRSS')
        self.sapclass.add_to_loadcombo('SPECXY', specx, 1, adding_combo=False)
        self.sapclass.add_to_loadcombo('SPECXY', specy, 1, adding_combo=False)
        self.sapclass.SapModel.RespCombo.SetNote("SPECXY", "Run the analysis and adjust the factor to scale the base shear to 80%/100% of static procedure")