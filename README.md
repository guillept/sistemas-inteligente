# mars-explorer
School assignment - Multi Agent System collecting stuff on Mars

## Run me

```bash
python main.py --help
usage: main.py [-h] [--obstacles OBSTACLES] [--rocks ROCKS]
               [--explorers EXPLORERS] [--carriers CARRIERS]

optional arguments:
  -h, --help            show this help message and exit
  --obstacles OBSTACLES
  --rocks ROCKS
  --explorers EXPLORERS
  --carriers CARRIERS

```

All params have defaults.

## Details

### Explorers

* can carry 1 rock
* know where the base is
* can sense nearby rocks
* can sense if they are "on" a rock or the base

### Carriers

* can carry any number of rocks
* can go to an explorer agent


## Modes

### No carriers

Explorers wander about, for every rock found they take it to the base.

    To run in this mode, you need to pass `--carriers 0`.


### With carriers

Explorers wander about. When they find a rock, they stop, send a message to all carriers
and one or more carriers will come to pick up the rock. Then the explorer carries on with
the search. When all the rocks are collected, the carriers go to the base to turn in their
rocks.
