# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['np_workflows',
 'np_workflows.experiments',
 'np_workflows.experiments.task_trained_network',
 'np_workflows.experiments.task_trained_network.camstim_scripts',
 'np_workflows.models',
 'np_workflows.shared']

package_data = \
{'': ['*'], 'np_workflows': ['assets/images/*']}

install_requires = \
['ipylab>=0.6.0,<0.7.0',
 'ipywidgets>=7,<8',
 'jupyter-scheduler>=1.2.0,<2.0.0',
 'jupyterlab-git>=0.41.0,<0.42.0',
 'jupyterlab>=3.6,<4.0',
 'np_datajoint',
 'np_probe_targets',
 'np_services>=0.1.33',
 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'np-workflows',
    'version': '1.3.17',
    'description': 'Ecephys and behavior workflows for the Mindscope Neuropixels team.',
    'long_description': '# np_workflows',
    'author': 'Ben Hardcastle',
    'author_email': 'ben.hardcastle@alleninstitute.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
