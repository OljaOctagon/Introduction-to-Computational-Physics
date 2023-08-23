from jinja2 import Environment, FileSystemLoader
import numpy as np

npart = 225
npatch = 5
natoms = npart * (npatch + 1)
nbonds = npart * npatch
nangles = npart * npatch
# diameter of core
sigma = 1

lx2 = 10
ly2 = lx2
lz2 = 0.5

context = {
    "number_of_atoms": natoms,
    "number_of_bonds": nbonds,
    "number_of_angles": nangles,
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

ru = sigma / 2
alpha = (108 / 180) * np.pi
mu = (72 / 180) * np.pi

ax = ru * np.sin(mu / 2)
ay = ru * np.cos(mu / 2)

bx = ru * np.sin(alpha / 2)
by = ru * np.cos(alpha / 2)

patch_center_distance = {
    1: (-ax, -ay),
    2: (ax, -ay),
    3: (bx, by),
    4: (0, ru),
    5: (-bx, by),
}

arr = np.array([[-ax, -ay], [ax, -ay], [bx, by], [0, ru], [-bx, by]])
for v in arr:
    assert np.linalg.norm(v) == ru

atoms = []
bonds = []
angles = []
for i in range(npart):
    xcore, ycore = np.random.rand(2) * 2 * lx2 - lx2
    zcore = 0

    core_id = i * (npatch + 1) + 1

    core_atom = {
        "atom_id": core_id,
        "mol_id": i + 1,
        "atom_type": 1,
        "charge": 1,
        "x": xcore,
        "y": ycore,
        "z": zcore,
    }

    atoms.append(core_atom)

    for j in range(1, npatch + 1):
        patch_id = core_id + j
        patch_atom = {
            "atom_id": patch_id,
            "mol_id": i + 1,
            "atom_type": 2,
            "charge": 1,
            "x": xcore + patch_center_distance[j][0],
            "y": ycore + patch_center_distance[j][1],
            "z": zcore,
        }
        atoms.append(patch_atom)

        bond = {
            "id": i * npatch + j,
            "bond_type": 1,
            "atom_1": core_id,
            "atom_2": patch_id,
        }
        bonds.append(bond)

        angle = {
            "id": i + 1,
            "angle_type": 1,
            "atom_1": core_id + j,
            "atom_2": core_id,
            "atom_3": core_id + (j % npatch) + 1,
        }

        angles.append(angle)


context["atoms"] = atoms
context["bonds"] = bonds
context["angles"] = angles

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template_start.txt")

filename = "starting_state.txt"
with open(filename, mode="w") as output:
    output.write(template.render(context))
