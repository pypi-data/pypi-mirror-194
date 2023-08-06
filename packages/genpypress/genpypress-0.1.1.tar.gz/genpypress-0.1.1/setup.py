# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genpypress', 'genpypress.mapping', 'genpypress.table']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0', 'cattrs>=22.2.0,<23.0.0']

setup_kwargs = {
    'name': 'genpypress',
    'version': '0.1.1',
    'description': 'Set of tools and utilities connected with press code generator.',
    'long_description': '# genpypress\n\nThis library contains several code generator helpers. It is connected to the `press` code generator.\n\n## Usage\n\n```python\nfrom pathlib import Path\nfrom genpypress import mapping\n\n# import a file in markdown format\nfile = Path("TGT_ACCS_METH_RLTD_906_900_915_AMR_NIC_PCR_2_M2C.md", encoding="utf-8")\nmap = mapping.from_markdown(file.read_text(encoding="utf-8"))\n\n# access table mapping property\nprint("Type of historization:", map.etl_historization)\n\n# access a column mapping property (case insensitive)\nprint("hist_type =", map["hist_type"].transformation_rule)\n\n# nonexisting column will - of course - blow the code up\ntry:\n    print(map["not available"])\nexcept KeyError as err:\n    print(f"error: {err}")\n```',
    'author': 'Jan Herout',
    'author_email': 'jan.herout@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
