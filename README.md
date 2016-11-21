# carrom-agent
Deterministic algorithm to simulate a carrom agent to play carrom

I have implemented a deterministic algorithm for playing carrom. It covers the complete board in 24 turns when averaged over 500 different random seeds.

Command for running the code:

python start_experiment.py -ne 500 for running over 500 different random seeds.

python start_experiment.py for random seed=0

python start_experiment.py -v 1 to visualise the carrom board

This has been done as a part of CS 747 course project.

The implementation of the board has been used from:

https://github.com/samiranrl/Carrom_rl

Algorithm:

It predicts the action to be taken given a state of the board. It checks for direct shots into pockets, then the cut shots, rebounds and the double shots (direct hit the coin so that the wall reflects it into the pocket) The algorithm uses theory of collisions to make correct moves.

The action consists of:

Position of the striker (normalized to be between 0 to 1)

Angle of strike ( constrained to be between -45 to 225)

Force( 0 to 1) 0 force covers almost one third the width of the board, force=1 covers 3.5 times the width of the board when noise is absent.

The algorithm successfully clears the board in 24 moves when averaged over 500 games.
