# Equivalent circuit model

This repository contains Python code for running an equivalent circuit model (ECM) developed for a 2013 Nissan Leaf battery cell and module. The `ecm` package contains source code for the equivalent circuit model while the `examples` folder provides scripts for running the ECM for a battery cell, module, and pack. Model parameters are determined from hybrid pulse power characterization (HPPC) and discharge tests conducted at ORNL. The battery cell and module specifications were provided by NREL.

## Installation

The [Anaconda](https://www.anaconda.com) or [Miniconda](https://conda.io/miniconda.html) distribution of Python 3 is recommended for this project. The `ecm` package requires Matplotlib, NumPy, Pandas, and SciPy.

The simplest way to install the ECM package is with pip. This can be done from within the equiv-circ-model directory:

```bash
# Install the ecm package
pip install -e .
```

A requirements file is provided for running the ECM in a virtual environment using pip:

```bash
# Create a new virtual environment
python -m venv env

# Activate the environment
source env/bin/activate

# Install packages needed for the ECM
pip install -r requirements.txt

# From within equiv-circ-model directory, install the ecm package
pip install -e .

# Deactivate the environment
deactivate

# Remove the environment by deleting the `env` folder
```

An environment yaml file is also provided for running the ECM in a conda environment:

```bash
# Create a new conda environment and install packages needed for the ECM
conda env create -f environment.yml

# Activate the environment
conda activate ecm

# From within equiv-circ-model directory, install the ecm package
pip install -e .

# Deactivate the environment
conda deactivate

# Remove the environment and its installed packages
conda env remove -n ecm
```

## Usage

Examples of using the `ecm` package are provided in the `examples` folder. From within the examples folder, each script can be run from the command line such as:

```bash
# View plots of the battery cell HPPC data
python view_cell_hppc_data.py

# Run the ECM for a battery cell and compare to HPPC data
python run_cell_hppc_ecm.py
```

## Project structure

**ecm** - Python package containing source code for the equivalent circuit model (ECM).

**examples** - Scripts for running various components of the ECM.

**examples/data** - Battery test data from a 2013 Nissan Leaf battery cell and module. This data is used for developing and validating the ECM.

**examples/params.py** - Parameters for the 2013 Nissan Leaf battery cell..

## Contributing

Comments, suggestions, and other feedback can be submitted on the [Issues](https://github.com/batterysim/equiv-circ-model/issues) page.

## License

This code is available under the MIT License - see the [LICENSE](LICENSE) file for more information.
