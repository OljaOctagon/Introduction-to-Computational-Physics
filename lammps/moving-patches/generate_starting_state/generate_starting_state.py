from jinja2 import Environment, FileSystemLoader
import numpy as np

npart = 225
npatch = 2
natoms = npart * (npatch + 1)
nbonds = npart * npatch

lx2 = 10
ly2 = lx2
lz2 = 0.5

context = {
    "number_of_atoms": natoms,
    "number_of_bonds": nbonds,
    "number_of_angles": npart,
    "number_of_atom_types": 2,
    "number_of_bond_types": 1,
    "number_of_angle_types": 1,
    "xlo": -lx2,
    "xhi": lx2,
    "ylo": -lx2,
    "yhi": lx2,
    "zlo": -lz2,
    "zhi": lz2,
}

masses = [{"type": 1, "mass": 2.0}, {"type": 2, "mass": 0.5}]
context["masses"] = masses

atoms = []
for i in range(1, npart + 1):
    xcore, ycore = np.random.rand(2) * 2 * lx2 - lx2
    zcore = np.random.rand() * 2 * lz2 - lz2

    core_atom = {
        "atom_id": i * 3,
        "mol_id": i,
        "atom_type": 1,
        "x": xcore,
        "y": ycore,
        "z": zcore,
    }

    atoms.append(core_atom)

    for j in range(1, npatch + 1):
        a = 1  # needs to be changed to right distance
        b = 1  # needs to be changed to right distance

        patch_atom = {
            "atom_id": i * 3 + j,
            "mol_id": i,
            "atom_type": 2,
            "x": xcore + a,
            "y": ycore + b,
            "z": zcore,
        }

        atoms.append(patch_atom)


context["atoms"] = atoms
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template_start.txt")

filename = "starting_state.txt"
with open(filename, mode="w") as output:
    output.write(template.render(context))
