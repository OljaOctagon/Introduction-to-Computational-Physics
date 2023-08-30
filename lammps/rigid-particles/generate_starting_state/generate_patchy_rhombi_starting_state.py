from jinja2 import Environment, FileSystemLoader
import numpy as np

npart = 100
nparticles_per_side = 10
npatches_per_side = 1
n_sides = 4
natoms = npart * (nparticles_per_side + npatches_per_side) * n_sides

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
    "number_of_atom_types": 2,
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


# for dma-as2
def get_patch_positions_one_patch_per_side(delta, n_sides, alpha, side_length):
    h2 = side_length * np.sin(alpha) / 2
    x = h2 * np.tan(alpha / 2)

    edges = np.array(
        [[-x, -h2], [side_length - x, -h2], [x, h2], [x - side_length, h2]]
    )

    pos_patches = []
    # dma-as1
    for i in range(n_sides):
        xpatch = edges[i][0] + delta * (edges[(i + 1) % n_sides][0] - edges[i][0])
        ypatch = edges[i][1] + delta * (edges[(i + 1) % n_sides][1] - edges[i][1])

        pos_patches.append([xpatch, ypatch])

    return pos_patches


atoms = []
molecules = []
edges = get_rhombi_edges(side_length, alpha)
delta = 0.2
pos_patches = get_patch_positions_one_patch_per_side(
    delta, n_sides, alpha, side_length + sigma * 2
)

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

            atom_id = i * (nparticles_per_side + 1) * n_sides + j * n_sides + m + 1
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

    for m in range(n_sides):
        patch_id = (
            i * (nparticles_per_side + 1) * n_sides
            + (nparticles_per_side) * n_sides
            + m
            + 1
        )

        patchx = xcenter + pos_patches[m][0]
        patchy = ycenter + pos_patches[m][1]
        patchz = zcenter
        patch_i = {
            "atom_id": patch_id,
            "atom_type": 2,
            "mol_id": 1,
            "charge": 1,
            "x": patchx,
            "y": patchy,
            "z": patchz,
        }
        molecule_i = {"atom_id": patch_id, "mol_id": mol_id}

        atoms.append(patch_i)
        molecules.append(molecule_i)


context["atoms"] = atoms
context["molecules"] = molecules

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template_start.txt")

filename = "starting_state.txt"
with open(filename, mode="w") as output:
    output.write(template.render(context))
