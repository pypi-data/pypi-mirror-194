from rich.console import Console
from rich.theme import Theme
from sap2000.display import generate_table
from sap2000.constants import REBARS

custom_theme = Theme({'success': 'green', 'error': 'bold red'})
console = Console(theme=custom_theme)


class Materials:
    def __init__(self, sapclass, log):
        self.sapclass = sapclass
        self.log = log
    
    def __str__(self) -> str:
        f"Typical Routines class"
    
    def __repr__(self) -> str:
        f"Materials(sapclass=\"{self.sapclass}\", log=\"{self.log}\")"

    def setup_nwt_concrete_material(self, name:str, fc:float):
        """Creates a New material with the specified fc per CSA A23.3 Section 8

        Args:
            name (str): Name of the material
            fc (float): Compressive strength of concrete
        """
        self.sapclass.change_units(unit_type="n_mm_c")
        SapModel = self.sapclass.SapModel
        SapModel.PropMaterial.SetMaterial(name, 2)      #Material Name and Type
        SapModel.PropMaterial.SetOConcrete_1(name, fc,False, 0.0, 2, 2, 0.00221914, 0.005, -0.1, 0.0, 0.0, 0)

        E = (3300 * (fc** 0.5) + 6900)*((2400/2300)**1.5)
        poisson = 0.2
        g = E/(2*(1+poisson))
        SapModel.PropMaterial.SetMPIsotropic(name, E, poisson, 9.899999527931235e-06, g)
        m = 2.4e-6
        SapModel.PropMaterial.SetWeightAndMass(name, m*9810, m)

    def template_rebar_setup(self):
        SapModel = self.sapclass.SapModel
        self.sapclass.unlock()

        #Delete unneccessary bars
        _, bar_info, _ = SapModel.PropRebar.GetNameList()
        [SapModel.PropRebar.Delete(bar) for bar in bar_info if not bar.endswith('M')]

        #Add missing bar info
        _, bar_info, _ = SapModel.PropRebar.GetNameList()
        
        self.sapclass.change_units(unit_type =list(REBARS.values)[0].unit)
        [self.add_rebar(name, prop.area, prop.dia) for name, prop in REBARS.items() if not name in bar_info]

    def add_rebar(self, name: str, area:float, diameter:float):
        self.sapclass.SapModel.PropRebar.SetProp(name, area, diameter)

    def template_conc_material_setup(self):
        self.sapclass.unlock()
        self.setup_nwt_concrete_material("CSA-M20",20)
        self.setup_nwt_concrete_material("CSA-M20",20)
        self.setup_nwt_concrete_material("CSA-M25",25)
        self.setup_nwt_concrete_material("CSA-M30",30)
        self.setup_nwt_concrete_material("CSA-M35",35)
        self.setup_nwt_concrete_material("CSA-M40",40)