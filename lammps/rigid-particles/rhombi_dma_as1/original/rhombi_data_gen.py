from src.patch import *
from math import pi


p = patch(0.7)
p.dim = 2
p.extratype = 1
p.style = "sphere"
p.extra = "Molecules"
p.seed = 543216
p.build(100, "patchy_rhombi", pi/3, 1, 16, 2, 0.7)
p.write("patchy_rhombi_delta=0.5_N=100_vfrac=0.7.data")


