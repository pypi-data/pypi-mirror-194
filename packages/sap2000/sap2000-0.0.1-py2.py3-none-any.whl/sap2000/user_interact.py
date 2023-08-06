from rich.prompt import Prompt, Confirm
from dataclasses import dataclass
from typing import Optional

@dataclass
class ResponseSpectrumFunction:
    name: str
    pga: float
    s02: float
    s05: float
    s1: float
    s2: float
    s5: float
    s10: float
    siteclass: int
    dampingratio: float
    f02: Optional[float] = 1
    f05: Optional[float] = 1
    f1: Optional[float] = 1
    f5: Optional[float] = 1
    f10: Optional[float] = 1

@dataclass
class SeismicParameters:
    Rd: float
    Ro: float
    Ie: float

def _ui_get_response_spectrum_function_values(self) -> ResponseSpectrumFunction:
    siteclass_map = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6 }
    name = Prompt.ask("The name for the respose spectrum function")
    pga = float(Prompt.ask("PGA value"))
    s02 = float(Prompt.ask("Spectral Acceleration for 0.2 second period"))
    s05 = float(Prompt.ask("Spectral Acceleration for 0.5 second period"))
    s1 = float(Prompt.ask("Spectral Acceleration for 1 second period"))
    s2 = float(Prompt.ask("Spectral Acceleration for 2 second period"))
    s5 = float(Prompt.ask("Spectral Acceleration for 5 second period"))
    s10 = float(Prompt.ask("Spectral Acceleration for 10 second period"))
    siteclass = siteclass_map[Prompt.ask("Site Class", choices=list("ABCDEF"), default="C")]
    if siteclass == 6:
        f02 = float(Prompt.ask("Site coefficient for 0.2 second period"))
        f05 = float(Prompt.ask("Site coefficient for 0.5 second period"))
        f1 = float(Prompt.ask("Site coefficient for 1 second period"))
        f2 = float(Prompt.ask("Site coefficient for 2 second period"))
        f5 = float(Prompt.ask("Site coefficient for 5 second period"))
        f10 = float(Prompt.ask("Site coefficient for 10 second period"))
    dampingratio = float(Prompt.ask("Damping Ratio"))

    if siteclass == 6:
        return ResponseSpectrumFunction(name=name, pga=pga, s02=s02, s05=s05, s1=s1, s2=s2, s5=s5, s10=s10, siteclass=siteclass, f02=f02, f05=f05, f1=f1, f2=f2, f5=f5, f10=f10, dampingratio=dampingratio)
    else:
        return ResponseSpectrumFunction(name=name, pga=pga, s02=s02, s05=s05, s1=s1, s2=s2, s5=s5, s10=s10, siteclass=siteclass, dampingratio=dampingratio)


def _ui_get_seismic_parameters() -> SeismicParameters:
    return SeismicParameters(
        Rd=float(Prompt.ask("Seismic Ductility Factor, Rd")),
        Ro=float(Prompt.ask("Seismic Overstrength Factor, Ro")),
        Ie=float(Prompt.ask("Seismic Importance Factor, Ie value"))
    )