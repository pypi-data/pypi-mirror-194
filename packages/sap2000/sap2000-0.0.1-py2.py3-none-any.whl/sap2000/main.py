from sap2000.model import Sap
from sap2000.Base.tables import Table
from sap2000.Base.units import Units
# from sap2000.modal import ModalAnalysis
# from sap2000.response_spectrum import ResponseSpectrum
# from sap2000.routines import Routines
# from sap2000.materials import Materials
# from sap2000.results import Results


def attach() -> Sap:
    """Returns a new SAP OAPI Class attached to the current opened SAP model.
    """
    sap = Sap()
    sap.Table = Table(sapclass=sap)
    sap.Units = Units(sapclass=sap)
    # sap.ModalAnalysis = ModalAnalysis(sapclass=sap, log=sap.log)
    # sap.ResponseSpectrum = ResponseSpectrum(sapclass=sap, log=sap.log)
    # sap.Routines = Routines(sapclass=sap, log=sap.log)
    # sap.Materials = Materials(sapclass=sap, log=sap.log)

    return sap
