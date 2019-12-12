# Equivalent circuit model

This repository contains Python code for running an equivalent circuit model (ECM) developed for a 2013 Nissan Leaf battery cell. Model parameters are determined from hybrid pulse power characterization (HPPC) tests conducted at ORNL. The battery cell and its specifications were provided by NREL.

## Installation

The [Anaconda][] or [Miniconda][] distribution of Python 3.7 is recommended for this project. After setting up Python, the following packages are required: Matplotlib, NumPy, Pandas, and SciPy.

## Usage

The main entry point for the program is `__main__.py` which is located in the `ecm` package. To execute the equivalent circuit model, clone this project then run the following terminal command from within the repository:

```bash
$ python ecm --vbatt
```

Use the help command to view the other command line options:

```bash
$ python ecm --help

usage: ecm [-h] [-vd] [-vh] [-cv] [-rc] [-so] [-vb]

optional arguments:
  -h, --help       show this help message and exit
  -vd, --viewdis   view discharge data
  -vh, --viewhppc  view hppc data
  -cv, --curvefit  curve fit hppc data
  -rc, --rctau     rc params from hppc data
  -so, --sococv    soc and ocv from hppc data
  -vb, --vbatt     ecm voltage from hppc data
```

## Project structure

**data** - This folder contains the experiment data for developing the ECM.

**ecm** - Python package containing components of the ECM.

**ecm/params.py** - Parameters that define the battery cell along with other variables needed to run the model.

## Contributing

Comments, suggestions, and other feedback can be submitted on the [Issues](https://github.com/batterysim/equiv-circ-model/issues) page.

## License

This code is available under the MIT License - see the [LICENSE](LICENSE) file for more information.

[anaconda]: https://www.anaconda.com
[miniconda]: https://conda.io/miniconda.html
