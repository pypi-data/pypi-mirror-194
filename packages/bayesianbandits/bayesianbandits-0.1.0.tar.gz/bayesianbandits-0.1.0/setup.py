# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bayesianbandits']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=1.2.1,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'typing-extensions>=4.5.0,<5.0.0']

setup_kwargs = {
    'name': 'bayesianbandits',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `bayesianbandits`\n\nbayesianbandits is a Pythonic framework for building agents to maximize rewards in multi-armed bandit (MAB) problems. These agents can handle a number of MAB subproblems, such as contextual, restless, and delayed reward bandits.\n\nBuilding an agent is as simple as defining arms and using the necessary decorators. For example, to create an agent for a Bernoulli bandit:\n\n```python\nimport numpy as np\n\nfrom bayesianbandits import contextfree, bandit, epsilon_greedy, Arm, DirichletClassifier\n\ndef reward_func(x):\n    return np.take(x, 0, axis=-1)\n\ndef action1_func():\n    # do action 1\n    ...\n\ndef action2_func():\n    # do action 2\n    ...\n\n@contextfree\n@bandit(learner=DirichletClassifier({"yes": 1.0, "no": 1.0}), policy=epsilon_greedy(0.1))\nclass Agent:\n    arm1 = Arm(action1_func, reward_func)\n    arm2 = Arm(action2_func, reward_func)\n\nagent = Agent()\n\nagent.pull() # receive some reward\nagent.update("yes") # update with observed reward\n\n```\n\n## Getting Started\n\nInstall this package from PyPI.\n\n```\npip install -U bayesianbandits\n```',
    'author': 'Rishi Kulkarni',
    'author_email': 'rishi@kulkarni.science',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
