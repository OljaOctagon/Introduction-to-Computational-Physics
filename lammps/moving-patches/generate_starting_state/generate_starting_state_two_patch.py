from jinja2 import Environment, FileSystemLoader
import numpy as np

# Number of central particles
npart = 225
# Number of patches
npatch = 2
# Number of atoms
natoms = npart * (npatch + 1)
# Number of bonds
nbonds = npart * npatch
# Number of angles
nangles = npart

# LJ diameter of central particle
sigma = 1

lx2 = 10
ly2 = lx2
lz2 = 0.5

rho = npart / (2 * lx2 * 2 * ly2 * 2 * lz2)
print("number density central particles: ", rho)

volume_sphere = 4 * np.power(sigma / 2, 3) * np.pi / 3
packing = rho * volume_sphere
print("packing fraction central particles: ", packing)

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

# LJ radius of central particle
r = sigma / 2

# distance vector between partilces and center.
# side note: here all patchy particles have same orientation
patch_center_distance = {
    1: (r, 0),
    2: (-r, 0),
}

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
        "atom_1": core_id + 1,
        "atom_2": core_id,
        "atom_3": core_id + 2,
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
