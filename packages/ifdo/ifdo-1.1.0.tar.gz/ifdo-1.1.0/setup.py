# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ifdo']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'ifdo',
    'version': '1.1.0',
    'description': 'iFDO utilities',
    'long_description': '# ifdo-py\n\nifdo-py is a Python library for the [iFDO](https://marine-imaging.com/fair/ifdos/iFDO-overview/) file format.\n\n## Install\n\n```bash\npip install ifdo\n```\n\n## Usage\n\n### Read/write iFDO files\n```python\nfrom ifdo import iFDO\n\n# Read from YAML file\nifdo_object = iFDO.load("path/to/ifdo.yaml")\n\n# Write to YAML\nifdo_object.save("path/to/ifdo.yaml")\n```\n\n### Create image annotations\n```python\nfrom datetime import datetime\nfrom ifdo.models import ImageAnnotation, AnnotationCoordinate, AnnotationLabel\n\n# Create a bounding box\ncoordinates = [\n    AnnotationCoordinate(x=0, y=0),\n    AnnotationCoordinate(x=1, y=0),\n    AnnotationCoordinate(x=1, y=1),\n    AnnotationCoordinate(x=0, y=1),\n]\n\n# Create a label for it\nlabel = AnnotationLabel(id="fish", annotator="kevin", created_at=datetime.now(), confidence=0.9)\n\n# Pack it into an annotation\nannotation = ImageAnnotation(coordinates=coordinates, labels=[label], shape=\'rectangle\')\n\n# Print it as a dictionary\nprint(annotation.to_dict())\n```\n\n```python\n{\n  \'coordinates\': [\n    {\'x\': 0, \'y\': 0}, \n    {\'x\': 1, \'y\': 0}, \n    {\'x\': 1, \'y\': 1}, \n    {\'x\': 0, \'y\': 1}\n  ], \n  \'labels\': [\n    {\n      \'id\': \'fish\', \n      \'annotator\': \'kevin\', \n      \'created-at\': datetime.datetime(2023, 2, 28, 16, 39, 46, 451290), \n      \'confidence\': 0.9\n    }\n  ], \n  \'shape\': \'rectangle\'\n}\n```',
    'author': 'Kevin Barnard',
    'author_email': 'kbarnard@mbari.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
