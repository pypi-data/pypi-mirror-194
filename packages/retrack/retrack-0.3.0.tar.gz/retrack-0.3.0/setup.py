# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['retrack',
 'retrack.engine',
 'retrack.engine.validators',
 'retrack.nodes',
 'retrack.utils']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0,<4.0', 'pandas>=1.5.2,<2.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'retrack',
    'version': '0.3.0',
    'description': 'A business rules engine',
    'long_description': '<p align="center">\n  <a href="https://github.com/gabrielguarisa/retrack"><img src="https://raw.githubusercontent.com/gabrielguarisa/retrack/main/logo.png" alt="retrack"></a>\n</p>\n<p align="center">\n    <em>A business rules engine</em>\n</p>\n\n<div align="center">\n\n[![Package version](https://img.shields.io/pypi/v/retrack?color=%2334D058&label=pypi%20package)](https://pypi.org/project/retrack/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/gabrielguarisa/retrack/releases)\n[![License](https://img.shields.io/github/license/gabrielguarisa/retrack)](https://github.com/gabrielguarisa/retrack/blob/main/LICENSE)\n\n</div>\n\n\n## Installation\n\n```bash\npip install retrack\n```\n\n## Usage\n\n```python\nimport retrack\n\n# Parse the rule/model\nparser = retrack.Parser(rule)\n\n# Create a runner\nrunner = retrack.Runner(parser)\n\n# Run the rule/model passing the data\nrunner(data)\n```\n\nThe `Parser` class parses the rule/model and creates a graph of nodes. The `Runner` class runs the rule/model using the data passed to the runner. The `data` is a dictionary or a list of dictionaries containing the data that will be used to evaluate the conditions and execute the actions. To see wich data is required for the given rule/model, check the `runner.request_model` property that is a pydantic model used to validate the data.\n\n### Creating a rule/model\n\nA rule is a set of conditions and actions that are executed when the conditions are met. The conditions are evaluated using the data passed to the runner. The actions are executed when the conditions are met.\n\nEach rule is composed of many nodes. To see each node type, check the [nodes](https://github.com/gabrielguarisa/retrack/tree/main/retrack/nodes) folder.\n\nTo create a rule, you need to create a JSON file with the following structure:\n\n```json\n{\n  "nodes": {\n\t\t"node id": {\n\t\t\t"id": "node id",\n\t\t\t"data": {},\n\t\t\t"inputs": {},\n\t\t\t"outputs": {},\n\t\t\t"name": "node name",\n\t\t},\n    // ... more nodes\n  }\n}\n```\n\nThe `nodes` key is a dictionary of nodes. Each node has the following properties:\n\n- `id`: The node id. This is used to reference the node in the `inputs` and `outputs` properties.\n- `data`: The node data. This is used as a metadata for the node.\n- `inputs`: The node inputs. This is used to reference the node inputs.\n- `outputs`: The node outputs. This is used to reference the node outputs.\n- `name`: The node name. This is used to define the node type.\n\nThe `inputs` and `outputs` properties are dictionaries of node connections. Each connection has the following properties:\n\n- `node`: The node id that is connected to the current node.\n- `input`: The input name of the connection that is connected to the current node. This is only used in the `inputs` property.\n- `output`: The output name of the connection that is connected to the current node. This is only used in the `outputs` property.\n\nTo see some examples, check the [examples](https://github.com/gabrielguarisa/retrack/tree/main/examples) folder.\n\n### Creating a custom node\n\nTo create a custom node, you need to create a class that inherits from the `BaseNode` class. Each node is a pydantic model, so you can use pydantic features to create your custom node. To see the available features, check the [pydantic documentation](https://pydantic-docs.helpmanual.io/).\n\nTo create a custom node you need to define the inputs and outputs of the node. To do this, you need to define the `inputs` and `outputs` class attributes. Let\'s see an example of a custom node that has two inputs, sum them and return the result:\n\n```python\nimport retrack\nimport pydantic\nimport pandas as pd\nimport typing\n\n\nclass SumInputsModel(pydantic.BaseModel):\n    input_value_0: retrack.InputConnectionModel\n    input_value_1: retrack.InputConnectionModel\n\n\nclass SumOutputsModel(pydantic.BaseModel):\n    output_value: retrack.OutputConnectionModel\n\n\nclass SumNode(retrack.BaseNode):\n    inputs: SumInputsModel\n    outputs: SumOutputsModel\n\n    def run(self, input_value_0: pd.Series,\n        input_value_1: pd.Series,\n    ) -> typing.Dict[str, pd.Series]:\n        output_value = input_value_0.astype(float) + input_value_1.astype(float)\n        return {\n            "output_value": output_value,\n        }\n```\n\nAfter creating the custom node, you need to register it in the nodes registry and pass the registry to the parser. Let\'s see an example:\n\n```python\nimport retrack\n\n# Register the custom node\nretrack.component_registry.register_node("sum", SumNode)\n\n# Parse the rule/model\nparser = Parser(rule, component_registry=retrack.component_registry)\n```\n\n## Contributing\n\nContributions are welcome! Please read the [contributing guidelines](https://github.com/gabrielguarisa/retrack/tree/main/CONTRIBUTING.md) first.',
    'author': 'Gabriel Guarisa',
    'author_email': 'gabrielguarisa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabrielguarisa/retrack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.16,<4.0.0',
}


setup(**setup_kwargs)
