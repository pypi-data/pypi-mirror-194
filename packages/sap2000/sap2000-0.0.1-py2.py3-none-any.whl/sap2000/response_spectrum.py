import pandas as pd
from rich.console import Console
from rich.theme import Theme
from sap2000.display import generate_table
from rich.live import Live

from sap2000.user_interact import (
    _ui_get_response_spectrum_function_values)

custom_theme = Theme({'success': 'green', 'error': 'bold red'})
console = Console(theme=custom_theme)


class ResponseSpectrum:
    def __init__(self, sapclass, log):
        self.sapclass = sapclass
        self.log = log
    
    def __str__(self) -> str:
        f"Response Spectrum procedures"
    
    def __repr__(self) -> str:
        f"ResponseSpectrum(sapclass=\"{self.sapclass}\", log=\"{self.log}\")"

    def create_function(self) -> str:
        """Sets up a Response Spectrum Function. Returns the name of the function.
        """
        p = _ui_get_response_spectrum_function_values()
        assert self.sapclass.SapModel.Func.FuncRS.SetNBCC2015(p.name, p.pga, p.s02, p.s05, p.s1, p.s2, p.s5, p.s10, p.siteclass, p.f02, p.f05, p.f1, p.f2, p.f5, p.f10, p.dampingratio) == 0
        return p.name

    def create_loadcase(self, direction: int, rs_function: str, Rd: float, Ro: float, Ie: float) -> str:
        loadcase_name = f"SPEC{direction}"
        scale_factor = 9.81 * Ie / (Rd*Ro)
        SapModel = self.sapclass.SapModel
        SapModel.LoadCases.ResponseSpectrum.SetCase(loadcase_name)
        SapModel.LoadCases.ResponseSpectrum.SetDampConstant(loadcase_name, 0.05)
        SapModel.LoadCases.ResponseSpectrum.SetDirComb(loadcase_name, 1, 1.2)   #Sets directional combination to SRSS
        SapModel.LoadCases.ResponseSpectrum.SetEccentricity(loadcase_name, 0.05)
        SapModel.LoadCases.ResponseSpectrum.SetLoads(loadcase_name, 1, (f"U{direction}"), (rs_function), (scale_factor), (""), (0))
        SapModel.LoadCases.ResponseSpectrum.SetModalCase(loadcase_name, "MODAL")
        SapModel.LoadCases.ResponseSpectrum.SetModalComb_1(loadcase_name, 1, 1.0, 0.0, 1)
        return loadcase_name
