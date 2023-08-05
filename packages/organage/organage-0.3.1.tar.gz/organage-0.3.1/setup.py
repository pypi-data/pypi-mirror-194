# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['organage',
 'organage.data',
 'organage.data.ml_models',
 'organage.data.ml_models.Covance',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Adipose',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Artery',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Brain',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Heart',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Immune',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Intestine',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Kidney',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Liver',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Lung',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Muscle',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Organismal',
 'organage.data.ml_models.Covance.Zprot_stableps_perf95.Pancreas',
 'organage.data.ml_models.KADRC',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaAdipose',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaArtery',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaBrain',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaHeart',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaImmune',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaIntestine',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaKidney',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaLiver',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaLung',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaMuscle',
 'organage.data.ml_models.KADRC.Zprot_stableps_perf95_fiba.DementiaPancreas']

package_data = \
{'': ['*'],
 'organage.data.ml_models.KADRC': ['Zprot_stableps_perf95/Adipose/*',
                                   'Zprot_stableps_perf95/Artery/*',
                                   'Zprot_stableps_perf95/Brain/*',
                                   'Zprot_stableps_perf95/Heart/*',
                                   'Zprot_stableps_perf95/Immune/*',
                                   'Zprot_stableps_perf95/Intestine/*',
                                   'Zprot_stableps_perf95/Kidney/*',
                                   'Zprot_stableps_perf95/Liver/*',
                                   'Zprot_stableps_perf95/Lung/*',
                                   'Zprot_stableps_perf95/Muscle/*',
                                   'Zprot_stableps_perf95/Organismal/*',
                                   'Zprot_stableps_perf95/Pancreas/*']}

install_requires = \
['dill>=0.3.6', 'pandas>=1.5.3', 'scikit-learn==1.0.2']

setup_kwargs = {
    'name': 'organage',
    'version': '0.3.1',
    'description': 'A package to pestimate organ-specific biological age using SomaScan plasma proteomics data',
    'long_description': '# organage\n\nA package to estimate organ-specific biological age using SomaScan plasma proteomics data\n\n## Installation\n\n```bash\n$ pip install organage\n```\n\n## Usage\n\n- see example\n\n## License\n\n`organage` was created by Hamilton Oh. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`organage` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Hamilton Oh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
