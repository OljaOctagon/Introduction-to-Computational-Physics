# Freezing Lennard-Jones at different densities.

For this assignment use the Lennard Jones tutorial https://lammpstutorials.github.io/sphinx/build/html/tutorials/lennardjones.html as starting point.
* Change the binary mixture (two particle types) to one particle type.
* Change the used number of particles to 500.
* Use three different densities, i.e 0.2,0.4 and 0.6. In the code as is you can set the box size and the number of particles, i.e the reduced density is given by rho^s = $sigma^3$\times (N/V), where N is the number of particles and V is the volume.
* For all three densities freeze the Lennard-Jones model by first equilibrating at the reduced temperature T=2.0 and then cooling down to the gas-solid phase separated region. Do that for the three different densities. Have a look at the phase diagram of Lennard-Jones to know how low you have to set the temperature T for each density.
* Calculate the radial pair distribution function with the help of the freud package for all three different densities, each one in the liquid state and one in the gas/solid state.
* Produce four plots, three for the three densities, that each contains the two radial distribution functions for the two temperatures; and a last plot where you plot all radial distribution functions (rdf) together in one plot. For each plot give a title, axis labels and legend and save the figures as pdf. Describe your observations.
