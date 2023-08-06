# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ztfquery', 'ztfquery.scripts', 'ztfquery.utils']

package_data = \
{'': ['*'], 'ztfquery': ['data/*']}

install_requires = \
['astropy>=5.2.1,<6.0.0',
 'matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0']

extras_require = \
{'dask': ['dask>=2023.2.0,<2024.0.0']}

setup_kwargs = {
    'name': 'ztfquery',
    'version': '1.24.4',
    'description': 'Python package to access ZTF data',
    'long_description': '# ztfquery\n\n[![PyPI](https://img.shields.io/pypi/v/ztfquery.svg?style=flat-square)](https://pypi.python.org/pypi/ztfquery)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1345222.svg)](https://doi.org/10.5281/zenodo.1345222)\n[![CI](https://github.com/mickaelrigault/ztfquery/actions/workflows/ci.yaml/badge.svg)](https://github.com/mickaelrigault/ztfquery/actions/workflows/ci.yaml)\n\nThis package is made to ease access to Zwicky Transient Facility data and data-products. It is maintained by M. Rigault (CNRS/IN2P3) and S. Reusch (DESY).\n\n[cite ztfquery](https://ui.adsabs.harvard.edu/abs/2018zndo...1345222R/abstract)\n\n# ztfquery: a python tool to access ztf (and SEDM) data\n\n`ztfquery` contains a list of tools:\n- **ZTF products:** a wrapper of the [IRSA web API](https://irsa.ipac.caltech.edu/docs/program_interface/ztf_api.html) that enable to get ztf data _(requires access for full data, but not public data)_:\n\t- Images and pipeline products, e.g. catalog ; See the [`ztfquery.query.py` documentation](doc/query.md)\n\t- LightCurves (not from image subtraction): See the  [`ztfquery.lightcurve.py` documentation](doc/lightcurve.md)\n\t- ZTF observing logs: See the  [`ztfquery.skyvision.py` documentation](doc/skyvision.md)\n\n- **Marshal/Fritz:** \nDownload the source information and data, such as lightcurves, spectra, coordinates and redshift:\n\t- from the [ZTF-I Marshal](http://skipper.caltech.edu:8080/cgi-bin/growth/marshal.cgi): See the [`ztfquery.marshal.py` documentation](doc/marshal.md)\n\t- from the [ZTF-II Fritz](https://fritz.science/): See the [`ztfquery.fritz.py` documentation](doc/fritz.md)\n\n- **SEDM Data:** tools to download SEDM data, including IFU cubes and target spectra, from [pharos](http://pharos.caltech.edu) \nSee the [`ztfquery.sedm.py` documentation](doc/sedm.md)\n\n- **ZTF alert:** Currently only a simple alert reader. See the [`ztfquery.alert.py` documentation](doc/alert.md)\n\n***\n\n# Credits\n\n## Citation\nMickael Rigault. (2018, August 14). ztfquery, a python tool to access ZTF data (Version doi). Zenodo. http://doi.org/10.5281/zenodo.1345222\n\n## Acknowledgments\nIf you have used `ztfquery` for a research you are publishing, please **include the following in your acknowledgments**:\n_"The ztfquery code was funded by the European Research Council (ERC) under the European Union\'s Horizon 2020 research and innovation programme (grant agreement n°759194 - USNAC, PI: Rigault)."_\n\n## Corresponding Authors:\n- M. Rigault: m.rigault@ipnl.in2p3.fr, CNRS/IN2P3\n- S. Reusch: simeon.reusch@desy.de, DESY\n\n***\n\n# Installation\n\nztfquery requires `python >= 3.8`\n\n## Install the code\nusing pip: `pip install ztfquery` (favored)\n\nor for the latest version:\n\ngo wherever you want to save the folder and then\n```bash\ngit clone https://github.com/MickaelRigault/ztfquery.git\ncd ztfquery\npoetry install\n```\n\n## Set your environment\n\nYou should also create the global variable `$ZTFDATA` (usually in your `~/.bash_profile` or `~/.cshrc`). Data you will download from IRSA will be saved in the directory indicated by `$ZTFDATA` following the IRSA data structure.\n\n## Login and Password storage\nYour credentials will requested the first time you need to access a service (IRSA, Marshal, etc.). They will then be stored, crypted, under ~/.ztfquery. \nUse `ztfquery.io.set_account(servicename)` to reset it.\n\nYou can also directly provide account settings when running `load_metadata` and `download_data` using the `auth=[your_username, your_password]` parameter. Similarly, directly provide the username and password to the ztf ops page when loading `NightSummary` using the `ztfops_auth` parameter.\n\n***\n\n# Quick Examples\n\n',
    'author': 'Mickael Rigault',
    'author_email': 'm.rigault@ipnl.in2p3.fr',
    'maintainer': 'Mickael Rigault',
    'maintainer_email': 'm.rigault@ipnl.in2p3.fr',
    'url': 'https://github.com/mickaelrigault/ztfquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
