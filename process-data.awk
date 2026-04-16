BEGIN { print "steps;L2;L2_rel;H1;H1_rel" }

/nan/ { next }
{ print $2 ";" $6 ";" $7 ";" $9 ";" $10 }
