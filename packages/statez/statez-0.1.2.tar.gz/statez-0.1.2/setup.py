# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statez']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'statez',
    'version': '0.1.2',
    'description': 'Helps you to build fancy statemachines',
    'long_description': '# statez\n\n![statez.png](https://raw.githubusercontent.com/4thel00z/logos/master/statez.png)\n\n## Motivation\n\nAll the statemachine packages for python look weird and do too much stuff.\nThis one is simple (and synchronous).\n\n\n## Installation\n\n```\npip install statez\n\n# or if you use poetry\npoetry add statez\n```\n\n## Usage\n\n```python\nfrom statez.core import (\n    Trigger,\n    From,\n    To,\n    Do,\n    StateMachine,\n    Event\n)\n\nif __name__ == \'__main__\':\n    s = StateMachine("HungryBoi", state="hungry")\n    transition = Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | Do(lambda a: True)\n    # It doesn\'t matter if you use the function directly or if you wrap it in Do :-)\n    assert transition == Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | (lambda a: True)\n    s += transition\n    s.consume(Event("Eat"))\n    assert s.state == "not_hungry", s.state\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/statez',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
