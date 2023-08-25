# GET FILE NAME FROM COMMAND LINE
set fname [lindex $argv 0]

# READ IN COORDINATES FROM FILE
mol new $fname type lammpstrj waitfor all step 1
mol modstyle 0 top "VDW" 1.0 15 

set sel0 [atomselect top "name 1"]
$sel0 set radius 0.300
$sel0 set color colorID 8

set sel1 [atomselect top "name 2"]
$sel1 set radius 0.1
$sel1 set color colorID 10

