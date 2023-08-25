# GET FILE NAME FROM COMMAND LINE
set fname [lindex $argv 0]

# READ IN COORDINATES FROM FILE
mol new $fname type lammpstrj waitfor all step 1
mol modstyle top 0  "DynamicBonds" 1.4 0.1 
