# Equivalent circuit model

An equivalent circuit model (ECM) developed for a 2013 Nissan Leaf battery cell. Model parameters are determined from hybrid pulse power characterization (HPPC) tests conducted at ORNL. The battery cell and its specifications were provided by NREL.

## Installation and usage

The [Anaconda](https://www.anaconda.com) or [Miniconda](https://conda.io/miniconda.html) distribution is recommended for the latest scientific Python stack. Requirements for this repository are listed below.

- Python 3.7.3
- Matplotlib
- NumPy
- Pandas
- SciPy

A command line interface to running the ECM or individual components of the model is provided by the `main.py` driver script. Example usage is shown below:

```bash
# Plot voltage from equivalent circuit model and compare to HPPC voltage
python main.py ecm

# Print and plot results for state of charge and open circuit voltage
python main.py soc
```

Run `python main.py -h` for available commands and options.

A Jupyter notebook, simply named `notebook.ipynb`, also demonstrates usage of the equivalent circuit model.

## Project structure

Experiment data for developing the ECM is located in the `data` folder. The model code is in the `ecmlib` Python package. Helper functions and model parameters are in the `utils` package.

## Contributing

Comments, suggestions, and other feedback can be submitted on the [Issues](https://github.com/batterysim/equiv-circ-model/issues) page.
