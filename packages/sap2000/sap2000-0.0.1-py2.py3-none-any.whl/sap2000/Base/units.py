import comtypes
import forallpeople as si
si.environment('structural', top_level=False)

class Units:
    def __init__(self, sapclass):
        self.sapclass = sapclass
    
    def __str__(self) -> str:
        f"Units procedures"
    
    def __repr__(self) -> str:
        f"Units(sapclass=\"{self.sapclass}\")"

    def get(self) -> tuple[si.Physical, si.Physical, str]:
        """Returns the current loaded Units in SAP2000

        Returns:
            tuple[si.Physical, si.Physical, str]: Returns forallpeople notation of Force, Distance and str notation of temperature (C/F)
        """
        return _get_from_sapobj(self.sapclass.SapModel)
    
    def set(self,unit_type: int) -> None:
        """Updates the current units in SAP model

        Args:
            unit_type (int): integer between 1 and 16; lb_in_F = 1, lb_ft_F = 2, kip_in_F = 3, kip_ft_F = 4, kN_mm_C = 5, kN_m_C = 6, kgf_mm_C = 7, kgf_m_C = 8, N_mm_C = 9, N_m_C = 10, Ton_mm_C = 11, Ton_m_C = 12, kN_cm_C = 13, kgf_cm_C = 14, N_cm_C = 15, Ton_cm_C = 16

        Raises:
            Exception: Raises exception for invalid unit_type
        """
        if unit_type > 0 and unit_type < 17 and type(unit_type) == int:
            ret = self.sapclass.SapModel.SetPresentUnits(unit_type)
            if ret == 0:
                print(f'Unittype successfully changed to type: {unit_type}')
                
            else:
                print(f'Unable to update units to type: {unit_type}')
        else:
            raise Exception("Wrong value for `unit_type`")
        
def _get_from_sapobj(SapModel: comtypes.POINTER) -> tuple[si.Physical, si.Physical, str]:
    """Returns the current loaded Units in SAP2000

    Args:
        SapModel (comtypes.POINTER): SapModel Object

    Returns:
        tuple[si.Physical, si.Physical, str]: Returns forallpeople notation of Force, Distance and str notation of temperature (C/F)
    """
    G = 9.80665 * si.m / (si.s**2)
    UNITS = [
        (si.lb, si.inch, "F"),
        (si.lb, si.ft, "F"),
        (si.kip, si.inch, "F"),
        (si.kip, si.ft, "F"),
        (si.kN, si.mm, "C"),
        (si.kN, si.m, "C"),
        (G * si.kg, si.mm, "C"),
        (G * si.kg, si.m, "C"),
        (si.N, si.mm, "C"),
        (si.N, si.m, "C"),
        (G * si.kg * 1000, si.mm, "C"),
        (G * si.kg * 1000, si.m, "C"),
        (si.kN, si.mm * 10, "C"),
        (G * si.kg, si.mm * 10, "C"),
        (si.N, si.mm * 10, "C"),
        (G * si.kg * 1000, si.mm * 10, "C"),
    ]
    return UNITS[SapModel.GetDatabaseUnits() - 1]