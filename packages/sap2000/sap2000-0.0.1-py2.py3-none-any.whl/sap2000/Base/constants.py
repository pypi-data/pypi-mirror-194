#!/usr/bin/env python
from dataclasses import dataclass
from typing import Optional

class SapDefinitions:
  FRAME_TYPES = {"PortalFrame" : 0, "ConcentricBraced" : 1, "EccentricBraced" : 2}
  UNITS = {
    "lb_in_f" : 1, "lb_ft_f" : 2, "kip_in_f" : 3, "kip_ft_f" : 4, "kn_mm_f" : 5, 
    "kn_m_c" : 6, "kgf_mm_c" : 7, "kgf_m_c" : 8, "n_mm_c" : 9, "n_m_c" : 10, 
    "ton_mm_c" : 11, "ton_m_c" : 12, "kn_cm_c" : 13, "kgf_cm_c" : 14, "n_cm_c" : 15,
    "ton_cm_c" : 16
    }

  MATERIAL_TYPES = {"MATERIAL_STEEL" : 1, "MATERIAL_CONCRETE" : 2, "MATERIAL_NODESIGN" : 3,
    "MATERIAL_ALUMINUM" : 4, "MATERIAL_COLDFORMED" : 5, "MATERIAL_REBAR" : 6, "MATERIAL_TENDON" : 7}

  STEEL_SUBTYPES = {
    "MATERIAL_STEEL_SUBTYPE_ASTM_A36" : 1,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A53GrB" : 2,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A500GrB_Fy42" : 3,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A500GrB_Fy46" : 4,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A572Gr50" : 5,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A913Gr50" : 6,
    "MATERIAL_STEEL_SUBTYPE_ASTM_A992_Fy50" : 7,
    "MATERIAL_STEEL_SUBTYPE_CHINESE_Q235" : 8,
    "MATERIAL_STEEL_SUBTYPE_CHINESE_Q345" : 9,
    "MATERIAL_STEEL_SUBTYPE_INDIAN_Fe250" : 10,
    "MATERIAL_STEEL_SUBTYPE_INDIAN_Fe345" : 11,
    "MATERIAL_STEEL_SUBTYPE_EN100252_S235" : 12,
    "MATERIAL_STEEL_SUBTYPE_EN100252_S275" : 13,
    "MATERIAL_STEEL_SUBTYPE_EN100252_S355" : 14,
    "MATERIAL_STEEL_SUBTYPE_EN100252_S450" : 15}

  OBJECT_TYPES = {"points": 1, "frames": 2, "cables": 3, "tendons": 4, "areas": 5, "solids": 6, "links": 7}

  LOAD_PATTERN_TYPES = {
    'LTYPE_DEAD' : 1,
    'LTYPE_SUPERDEAD' : 2,
    'LTYPE_LIVE' : 3,
    'LTYPE_REDUCELIVE' : 4,
    'LTYPE_QUAKE' : 5,
    'LTYPE_WIND': 6,
    'LTYPE_SNOW' : 7,
    'LTYPE_OTHER' : 8,
    'LTYPE_MOVE' : 9,
    'LTYPE_TEMPERATURE' : 10,
    'LTYPE_ROOFLIVE' : 11,
    'LTYPE_NOTIONAL' : 12,
    'LTYPE_PATTERNLIVE' : 13,
    'LTYPE_WAVE': 14,
    'LTYPE_BRAKING' : 15,
    'LTYPE_CENTRIFUGAL' : 16,
    'LTYPE_FRICTION' : 17,
    'LTYPE_ICE' : 18,
    'LTYPE_WINDONLIVELOAD' : 19,
    'LTYPE_HORIZONTALEARTHPRESSURE' : 20,
    'LTYPE_VERTICALEARTHPRESSURE' : 21,
    'LTYPE_EARTHSURCHARGE' : 22,
    'LTYPE_DOWNDRAG' : 23,
    'LTYPE_VEHICLECOLLISION' : 24,
    'LTYPE_VESSELCOLLISION' : 25,
    'LTYPE_TEMPERATUREGRADIENT' : 26,
    'LTYPE_SETTLEMENT' : 27,
    'LTYPE_SHRINKAGE' : 28,
    'LTYPE_CREEP' : 29,
    'LTYPE_WATERLOADPRESSURE' : 30,
    'LTYPE_LIVELOADSURCHARGE' : 31,
    'LTYPE_LOCKEDINFORCES' : 32,
    'LTYPE_PEDESTRIANLL' : 33,
    'LTYPE_PRESTRESS' : 34,
    'LTYPE_HYPERSTATIC' : 35,
    'LTYPE_BOUYANCY' : 36,
    'LTYPE_STREAMFLOW' : 37,
    'LTYPE_IMPACT' : 38,
    'LTYPE_CONSTRUCTION' : 39,
  }

  def __init__(self):
    pass

  @staticmethod
  def _lookup(reference: dict, value ,reverse:bool):
    if not reverse:
      return reference.get(value)
    else:
      reverse_dict = {v:k for k,v in reference.items()}
      return reverse_dict.get(value)
    
  @staticmethod
  def _list_keys(reference: dict, reverse:bool) -> list:
    if reverse:
      return list(reference.values())
    else:
      return list(reference.keys())

  def frame_types(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.FRAME_TYPES, lookup_value, reverse_lookup)

  def list_frame_types(self, reverse:bool=False) -> list:
    return self._list_keys(self.FRAME_TYPES, reverse)
  
  def units(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.UNITS, lookup_value, reverse_lookup)

  def list_units(self, reverse:bool=False) -> list:
    return self._list_keys(self.UNITS, reverse)

  def material_types(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.MATERIAL_TYPES, lookup_value, reverse_lookup)

  def list_material_types(self, reverse:bool=False) -> list:
    return self._list_keys(self.MATERIAL_TYPES, reverse)

  def steel_subtypes(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.STEEL_SUBTYPES, lookup_value, reverse_lookup)

  def list_steel_subtypes(self, reverse:bool=False) -> list:
    return self._list_keys(self.STEEL_SUBTYPES, reverse)

  def object_types(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.OBJECT_TYPES, lookup_value, reverse_lookup)

  def list_object_types(self, reverse:bool=False) -> list:
    return self._list_keys(self.OBJECT_TYPES, reverse)

  def load_pattern_types(self, lookup_value, reverse_lookup:bool = False):
    return self._lookup(self.LOAD_PATTERN_TYPES, lookup_value, reverse_lookup)

  def list_pattern_types(self, reverse:bool=False) -> list:
    return self._list_keys(self.LOAD_PATTERN_TYPES, reverse)


@dataclass(frozen=True)
class Rebar:
  name: str
  dia: float
  area: float
  weight: float
  unit: Optional[str] = "kn_mm_c"

REBARS = {
  "10M":Rebar("10M", 11.3, 100., 7.698e-6),
  "15M":Rebar("15M", 16.0, 200., 1.54e-5),
  "20M":Rebar("20M", 19.5, 300., 2.309e-5),
  "25M":Rebar("25M", 25.2, 500., 3.849e-5),
  "30M":Rebar("30M", 29.9, 700., 5.389e-5),
  "35M":Rebar("35M", 35.7, 1000., 7.698e-5),
  "45M":Rebar("45M", 43.7, 1500., 11.55e-5),
  "55M":Rebar("55M", 56.6, 2500., 19.25e-5)
}