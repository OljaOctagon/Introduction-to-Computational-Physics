## Exercise 2: LJ dimers 

### 1 Dimers 
* Fix together two LJ dimers with fix rigid and freeze them via decreasing temperature (NVE or NVT ensemble). Start from 200 dimers, density = 0.6, temperature=1.5 (in reduced units). For temperature freezing run decrease T to 0.1. 
* Observe the freezing trajectory with vmd and make snapshots of the frozen dimers. Describe qualitatively what you observe. 
* Calculate the pair distribution function g(r) for the liquid state and the frozen states and describe your observations. 

### 2 Trimers (Optional)
* Fix together LJ spheres to form a pyramid and freeze them via decreasing temperature, using the same thermodynamic parameters as above.
* Calculate the g(r) of the single LJ spheres for the liquid state and the frozen state. 
* Inspect the trajectories with vmd and provide some snapshots. Describe what you observe.  
* Compare g(r) of the single LJ spheres for the liquid and the frozen state.

### 3  Comparing singlets, dimers and trimers 
* Compare the g(r) of the single LJ spheres of the singletts, dimers and trimers. What do you observe? 
* Find a way to calcualte the dimer-dimer and trimer-trimer radial pair distribtuion functions g_dd(r) and g_tt(r). 


# Exercise 3: LJ rhombi particles 
Use fix rigid to build 200 regular rhombi from LJ spheres. This thime we operate in Two-dimensions. for building the rhombi use 5,10 and 20 spheres per side length. Freeze the rhombi assembly again with the same procedure as in Exercise 2 and 3. 
* Inspect the trajectories with vmd and provide some snapshots. Describe what you observe. 
* Calculate the single sphere  g(r) and the rhombi-rhombi pair distribution function g_rr(r) and describe your observations. 




