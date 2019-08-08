# Equivalent circuit model

The repository contains Python code for running an equivalent circuit model (ECM) developed for a 2013 Nissan Leaf battery cell. Model parameters are determined from hybrid pulse power characterization (HPPC) tests conducted at ORNL. The battery cell and its specifications were provided by NREL.

## Installation and usage

The equivalent circuit model was developed with Python 3.7 and requires the following packages:

- Matplotlib
- NumPy
- Pandas
- SciPy

The main entry point for the program is `__main__.py` which is located in the `ecmlib` package. To execute the model, clone this repository then run the following command from within the repo:

```bash
python ecmlib --vbatt
```

Use the help command to view the other command line options:

```bash
python ecmlib --help
```

## Project structure

Experiment data for developing the ECM is located in the `data` folder. The model code is in the `ecmlib` Python package along with the parameters module `params.py` and various helper functions.

## Contributing

Comments, suggestions, and other feedback can be submitted on the [Issues](https://github.com/batterysim/equiv-circ-model/issues) page.
