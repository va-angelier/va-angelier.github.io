# Robot CLI – Usage

## Quick start
python -m robot.cli init
python -m robot.cli power on
python -m robot.cli navigate --to "Aisle 3"
python -m robot.cli charge start
python -m robot.cli status

## Commands
- power [on|off]
- navigate --to <location>
- charge [start|stop|status]
- logs [tail|export]

## Examples
# Command attempted during charging (expected: error)
python -m robot.cli navigate --to "Dock"
# -> ERROR: robot is charging; navigation rejected

## Exit codes
0=OK, 2=InvalidCommand, 3=StateViolation, 4=IOError
