#!/bin/sh
#
pre=/home/windyer/software/smog-2.5/bin/
$pre/smog_adjustPDB -i ../AF2/AF2_1.pdb -o AF2_adj.pdb

$pre/smog2 -i AF2_adj.pdb -CAgaussian -dname CA_gau -openSMOG
