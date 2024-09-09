from ase import Atoms
from pymatgen.analysis.structure_matcher import StructureMatcher
from pymatgen.io.cif import CifParser
from multiprocessing import Process
from typing import Dict

MATCHER = StructureMatcher(ltol=0.05, stol=0.1, angle_tol=5)
ENERGY_REF = {
    "Ne": -0.0259,
    "He": -0.0091,
    "Ar": -0.0688,
    "F": -1.9115,
    "O": -4.9467,
    "Cl": -1.8485,
    "N": -8.3365,
    "Kr": -0.0567,
    "Br": -1.553,
    "I": -1.4734,
    "Xe": -0.0362,
    "S": -4.1364,
    "Se": -3.4959,
    "C": -9.2287,
    "Au": -3.2739,
    "W": -12.9581,
    "Pb": -3.7126,
    "Rh": -7.3643,
    "Pt": -6.0711,
    "Ru": -9.2744,
    "Pd": -5.1799,
    "Os": -11.2274,
    "Ir": -8.8384,
    "H": -3.3927,
    "P": -5.4133,
    "As": -4.6591,
    "Mo": -10.8457,
    "Te": -3.1433,
    "Sb": -4.129,
    "B": -6.6794,
    "Bi": -3.8405,
    "Ge": -4.623,
    "Hg": -0.3037,
    "Sn": -4.0096,
    "Ag": -2.8326,
    "Ni": -5.7801,
    "Tc": -10.3606,
    "Si": -5.4253,
    "Re": -12.4445,
    "Cu": -4.0992,
    "Co": -7.1083,
    "Fe": -8.47,
    "Ga": -3.0281,
    "In": -2.7517,
    "Cd": -0.9229,
    "Cr": -9.653,
    "Zn": -1.2597,
    "V": -9.0839,
    "Tl": -2.3626,
    "Al": -3.7456,
    "Nb": -10.1013,
    "Be": -3.7394,
    "Mn": -9.162,
    "Ti": -7.8955,
    "Ta": -11.8578,
    "Pa": -9.5147,
    "U": -11.2914,
    "Sc": -6.3325,
    "Np": -12.9478,
    "Zr": -8.5477,
    "Mg": -1.6003,
    "Th": -7.4139,
    "Hf": -9.9572,
    "Pu": -14.2678,
    "Lu": -4.521,
    "Tm": -4.4758,
    "Er": -4.5677,
    "Ho": -4.5824,
    "Y": -6.4665,
    "Dy": -4.6068,
    "Gd": -14.0761,
    "Eu": -10.257,
    "Sm": -4.7186,
    "Nd": -4.7681,
    "Pr": -4.7809,
    "Pm": -4.7505,
    "Ce": -5.9331,
    "Yb": -1.5396,
    "Tb": -4.6344,
    "La": -4.936,
    "Ac": -4.1212,
    "Ca": -2.0056,
    "Li": -1.9089,
    "Sr": -1.6895,
    "Na": -1.3225,
    "Ba": -1.919,
    "Rb": -0.9805,
    "K": -1.1104,
    "Cs": -0.8954,
}


def get_e_form_per_atom(
    structure: Atoms, energy: float, ref: Dict[str, float] = ENERGY_REF
):
    comp = structure.get_chemical_symbols()
    natoms = len(comp)
    e_form = energy - sum(ref[ele] for ele in comp)
    return e_form / natoms


def read_file(fpth: str):
    cif = CifParser(fpth)
    # if cif.has_errors:
    #     raise ValueError("CIF file is not valid.")
    structure = cif.parse_structures(primitive=True)[0]
    if cif.check(structure) is not None:
        raise ValueError("CIF file is not valid.")
    return structure


def validate_cif(fpth: str, timeout: int=3):
    p = Process(target=read_file, args=(fpth,))
    p.start()
    p.join(timeout)
    if p.exitcode is None:
        p.kill()
        raise TimeoutError("Timeout to validate CIF file")
    elif p.exitcode != 0:
        raise ValueError("CIF file %s is not valid" % fpth)
