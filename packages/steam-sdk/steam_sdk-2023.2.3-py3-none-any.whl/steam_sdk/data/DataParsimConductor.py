from typing import (List, Dict)
from pydantic import BaseModel

############################
# General parameters
class GeneralParameters(BaseModel):
    magnet_name: str = None
    circuit_name: str = None
    state: str = None  # measured, deduced from short-samples, deduced from design

############################
# Magnet
class Magnet(BaseModel):
    coils: List[str] = []
    measured_inductance_versus_current: List[List[float]] = []

############################
# Coils
class Coil(BaseModel):
    ID: str = None
    cable_ID: str = None
    coil_length: float = None
    coil_RRR: float = None
    T_ref_RRR_low: float = None
    T_ref_RRR_high: float = None
    coil_resistance_room_T: float = None
    T_ref_coil_resistance: float = None
    conductors: List[str] = []  # TODO: make sure that names correspond to conductor instances
    weight_conductors: List[float] = []  # TODO: make sure the length is the same as of the list before

############################
# Conductors
class Conductor(BaseModel):
    ID: str = None
    shape: str = None # round, rectangular
    number_of_strands: int = None
    strand_diameter: float = None
    width: float = None
    height: float = None
    Cu_noCu: float = None
    RRR: float = None
    strand_twist_pitch: float = None
    filament_twist_pitch: float = None
    Ic_1: float = None
    T_ref_Ic_1: float = None
    B_ref_Ic_1: float = None
    Cu_noCu_sample_1: float = None
    Ic_2: float = None
    T_ref_Ic_2: float = None
    B_ref_Ic_2: float = None
    Cu_noCu_sample_2: float = None
    f_rho_eff: float = None
    Ra: float = None
    Rc: float = None

class DataParsimConductor(BaseModel):
    '''
        **Class for the STEAM magnet**

        This class contains the data structure of a Conductor parsim event analyzed with STEAM_SDK.

        :return: DataParsimConductor object
    '''

    GeneralParameters: GeneralParameters = GeneralParameters()
    Magnet: Magnet = Magnet()
    Coils: Dict[str, Coil] = {}
    Conductors: Dict[str, Conductor] = {}
