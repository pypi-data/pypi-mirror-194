# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtg_ontology', 'mtg_ontology.datamodel', 'mtg_ontology.schema']

package_data = \
{'': ['*']}

install_requires = \
['linkml-runtime>=1.1.24,<2.0.0']

setup_kwargs = {
    'name': 'mtg-ontology',
    'version': '0.1.0',
    'description': 'An ontology describing Magic: The Gathering.',
    'long_description': '# mtg-ontology\n\nAn ontology describing Magic: The Gathering.\n\n## Website\n\n* [https://cmdoret.net/mtg_ontology](https://cmdoret.net/mtg_ontology)\n\n## Repository Structure\n\n* [examples/](examples/) - example data\n* [project/](project/) - project files (do not edit these)\n* [src/](src/) - source files (edit these)\n    * [mtg_ontology](src/mtg_ontology)\n        * [schema](src/mtg_ontology/schema) -- LinkML schema (edit this)\n* [datamodel](src/mtg_ontology/datamodel) -- Generated python datamodel\n* [tests](tests/) - python tests\n\n## Developer Documentation\n\n<details>\nUse the `make` command to generate project artefacts:\n\n- `make all`: make everything\n- `make deploy`: deploys site\n\n</details>\n\n## Credits\n\nthis project was made with [linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)\n',
    'author': 'Cyril Matthey-Doret',
    'author_email': 'cmdoret@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
