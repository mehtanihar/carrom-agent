
max=10
j=50

for i in `seq 2 $max`
do
	k=$((j + 1))
	echo $k
	
	
	cmd="python start_experiment.py"
	$cmd
	sed -i "s/default=$j,help='Random Seed'/default=$k,help='Random Seed'/g" start_experiment.py
	j=$((j + 1))
	#cmd="python carrom_agent/parse_exp.py"
	#$cmd
done
j=$((j - 1))
sed -i "s/default=59,help='Random Seed'/default=50,help='Random Seed'/g" start_experiment.py

