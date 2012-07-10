cd $1
nohup ../src/moses/scripts/ems/experiment.perl -multicore -max-active 10 -no-graph -config config -exec >& OUT.1 &
