from jinja2 import Environment, FileSystemLoader
import numpy as np

npart = 100
nparticles_per_side = 4
n_sides = 4
natoms = npart * nparticles_per_side * n_sides

# side length of rhombi
side_length = 1
# angle of rhombi
alpha = np.pi / 3

# diameter of core
sigma = side_length / nparticles_per_side

lx2 = 20
ly2 = lx2
lz2 = sigma / 2

context = {
    "number_of_atoms": natoms,
    "number_of_atom_types": 1,
    "xlo": -lx2,
    "xhi": lx2,
    "ylo": -lx2,
    "yhi": lx2,
    "zlo": -lz2,
    "zhi": lz2,
}


def get_rhombi_edges(side_length, alpha):
    h2 = np.sin(alpha) / 2
    x = h2 * np.tan(alpha / 2)

    edges = np.array(
        [[-x, -h2], [side_length - x, -h2], [x, h2], [x - side_length, h2]]
    )

    return edges


atoms = []
molecules = []
edges = get_rhombi_edges(side_length, alpha)


for i in range(npart):
    # get random distribution of rhombi
    xcenter, ycenter = np.random.rand(2) * 2 * lx2 - lx2
    zcenter = 0

    for j in range(nparticles_per_side):
        for m in range(n_sides):
            bead_ix = (
                xcenter
                + edges[m][0]
                + (edges[(m + 1) % n_sides][0] - edges[m][0]) * j * sigma
            )
            bead_iy = (
                ycenter
                + edges[m][1]
                + (edges[(m + 1) % n_sides][1] - edges[m][1]) * j * sigma
            )
            bead_iz = zcenter

            atom_id = i * nparticles_per_side * n_sides + j * n_sides + m + 1
            mol_id = i + 1
            bead_i = {
                "atom_id": atom_id,
                "atom_type": 1,
                "mol_id": 1,
                "charge": 1,
                "x": bead_ix,
                "y": bead_iy,
                "z": bead_iz,
            }
            molecule_i = {"atom_id": atom_id, "mol_id": mol_id}

            atoms.append(bead_i)
            molecules.append(molecule_i)

context["atoms"] = atoms
context["molecules"] = molecules

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template_start.txt")

filename = "starting_state.txt"
with open(filename, mode="w") as output:
    output.write(template.render(context))
