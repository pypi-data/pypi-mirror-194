# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ztfparsnip']

package_data = \
{'': ['*'], 'ztfparsnip': ['BTS_plus_TDE/*']}

install_requires = \
['astro-parsnip>=1.3.1,<2.0.0',
 'h5py>=3.7.0,<4.0.0',
 'numpy>=1.24.0,<2.0.0',
 'pandas-stubs>=1.5.2.230105,<2.0.0.0',
 'pandas>=1.5.2,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'tqdm-stubs>=0.2.1,<0.3.0',
 'tqdm>=4.64.1,<5.0.0',
 'types-pyyaml>=6.0.12.8,<7.0.0.0']

entry_points = \
{'console_scripts': ['ztftrain = main:run']}

setup_kwargs = {
    'name': 'ztfparsnip',
    'version': '0.2.0',
    'description': 'Generate noisified lightcurves based on the BTS sample and retrain Parsnip with these.',
    'long_description': '# ztfparsnip\n[![CI](https://github.com/simeonreusch/ztfparsnip/actions/workflows/ci.yaml/badge.svg)](https://github.com/simeonreusch/ztfparsnip/actions/workflows/ci.yaml)\n[![Coverage Status](https://coveralls.io/repos/github/simeonreusch/ztfparsnip/badge.svg?branch=main)](https://coveralls.io/github/simeonreusch/ztfparsnip?branch=main)\n\nRetrain [Parsnip](https://github.com/LSSTDESC/parsnip) for ZTF. This is achieved by using [fpbot](https://github.com/simeonreusch/fpbot) forced photometry lightcurves of the [Bright Transient Survey](https://sites.astro.caltech.edu/ztf/bts/bts.php). These are augmented (redshifted, noisifed and - when possible - K-corrected).\n\nThe package is maintained by [A. Townsend](https://github.com/aotownsend) (HU Berlin) and [S. Reusch](https://github.com/simeonreusch) (DESY).\n\n## Usage\n### Create augmented training sample\n```python\nfrom pathlib import Path\nfrom ztfparsnip.create import CreateLightcurves\nweights = {"sn_ia": 9400, "tde": 9400, "sn_other": 9400, "agn": 9400, "star": 9400}\nsample = CreateLightcurves(\n        output_format="parsnip",\n        classkey="simpleclasses",\n        weights=weights,\n        train_dir=Path("train"),\n        plot_dir=Path("plot"),\n        seed=None,\n        phase_lim=True,\n        k_corr=True,\n    )\nsample.select()\nsample.create(plot_debug=False)\n```\n\n### Train Parsnip with the augmented sample\nRun `ztftrain INFILE` where `INFILE` points to a `.h5` object.\n\n### Evaluate\nComing soon.',
    'author': 'Simeon Reusch',
    'author_email': 'simeon.reusch@desy.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
