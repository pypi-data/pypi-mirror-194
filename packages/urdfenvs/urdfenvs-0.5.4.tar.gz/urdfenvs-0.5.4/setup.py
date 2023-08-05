# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['urdfenvs',
 'urdfenvs.keyboard_input',
 'urdfenvs.robots.albert',
 'urdfenvs.robots.boxer',
 'urdfenvs.robots.generic_urdf',
 'urdfenvs.robots.iris',
 'urdfenvs.robots.jackal',
 'urdfenvs.robots.prius',
 'urdfenvs.robots.tiago',
 'urdfenvs.scene_examples',
 'urdfenvs.sensors',
 'urdfenvs.urdf_common']

package_data = \
{'': ['*'],
 'urdfenvs.robots.albert': ['meshes/*',
                            'meshes/collision/*',
                            'meshes/visual/*'],
 'urdfenvs.robots.boxer': ['meshes/collision/*', 'meshes/visual/*'],
 'urdfenvs.robots.generic_urdf': ['dual_arm/*',
                                  'mobile_panda/*',
                                  'mobile_panda/meshes/collision/*',
                                  'mobile_panda/meshes/visual/*',
                                  'n_link/*',
                                  'panda/*',
                                  'panda/meshes/collision/*',
                                  'panda/meshes/visual/*',
                                  'point_robot/*'],
 'urdfenvs.robots.iris': ['meshes/*'],
 'urdfenvs.robots.jackal': ['meshes/*',
                            'meshes/collision/*',
                            'meshes/visual/*'],
 'urdfenvs.robots.prius': ['meshes/*'],
 'urdfenvs.robots.tiago': ['pal_gripper_description/meshes/*',
                           'pmb2_description/meshes/base/*',
                           'pmb2_description/meshes/meshes/*',
                           'pmb2_description/meshes/objects/*',
                           'pmb2_description/meshes/sensors/*',
                           'pmb2_description/meshes/wheels/*',
                           'tiago_description/meshes/arm/*',
                           'tiago_description/meshes/head/*',
                           'tiago_description/meshes/sensors/xtion_pro_live/*',
                           'tiago_description/meshes/torso/*',
                           'tiago_dual_description/meshes/torso/*'],
 'urdfenvs.scene_examples': ['obstacle_data/*'],
 'urdfenvs.urdf_common': ['meshes/*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0',
 'gym>=0.22,<0.23',
 'mpscenes>=0.3.1,<0.4.0',
 'numpy>=1.19,<1.24',
 'pybullet>=3.2.1,<4.0.0',
 'yourdfpy>=0.0.52,<0.0.53']

setup_kwargs = {
    'name': 'urdfenvs',
    'version': '0.5.4',
    'description': 'Simple simulation environment for robots, based on the urdf files.',
    'long_description': 'Generic URDF robots\n===================\n\nIn this package, generic urdf robots and a panda gym environment are\navailable. The goal is to make this environment as easy as possible to\ndeploy. Although, we used the OpenAI-Gym framing, these environments are\nnot necessarly restricted to Reinforcement-Learning but rather to local\nmotion planning in general.\n\n\n<table>\n <tr>\n  <td> Point Robot </td>\n  <td> Point Robot with Keyboard Input </td>\n  <td> Non-Holonomic Robot </td>\n </tr>\n <tr>\n  <td> <img src="/docs/source/img/pointRobot.gif" width="250" height="250"/> </td>\n  <td> <img src="/docs/source/img/pointRobotKeyboardInput.gif" width="250" height="250"/> </td>  \n  <td> <img src="/docs/source/img/boxerRobot.gif" width="250" height="250"/> </td>\n </tr>\n</table>\n\n<table>\n <tr>\n  <td> Tiago Robot </td>\n  <td> Tiago Robot with Keyboard Input </td>\n </tr>\n <tr>\n  <td> <img src="/docs/source/img/tiago.gif" width="250" height="250"/> </td>\n  <td> <img src="/docs/source/img/tiagoKeyboardInput.gif" width="250" height="250"/> </td>\n </tr>\n</table>\n\n<table>\n <tr>\n  <td> Panda Robot </td>\n  <td> Albert Robot </td>\n  </tr>\n <tr>\n  <td> <img src="/docs/source/img/panda.gif" width="250" height="250"/> </td>\n  <td> <img src="/docs/source/img/albert.gif" width="250" height="250"/> </td>\n  </tr>\n</table>\n\nGetting started\n===============\n\nThis is the guide to quickle get going with urdf gym environments.\n\nPre-requisites\n--------------\n\n-   Python \\>=3.8\n-   pip3\n-   git\n\nInstallation from pypi\n----------------------\n\nThe package is uploaded to pypi so you can install it using\n\n``` {.sourceCode .bash}\npip3 install urdfenvs\n```\n\nInstallation from source\n------------------------\n\nYou first have to download the repository\n\n``` {.sourceCode .bash}\ngit clone git@github.com:maxspahn/gym_envs_urdf.git\n```\n\nThen, you can install the package using pip as:\n\n``` {.sourceCode .bash}\npip3 install .\n```\n\nThe code can be installed in editible mode using\n\n``` {.sourceCode .bash}\npip3 install -e .\n```\n\nNote that we recommend using poetry in this case.\n\nOptional: Installation with poetry\n----------------------------------\n\nIf you want to use [poetry](https://python-poetry.org/docs/), you have\nto install it first. See their webpage for instructions\n[docs](https://python-poetry.org/docs/). Once poetry is installed, you\ncan install the virtual environment with the following commands. Note\nthat during the first installation `poetry update` takes up to 300 secs.\n\n``` {.sourceCode .bash}\npoetry install\n```\n\nThe virtual environment is entered by\n\n``` {.sourceCode .bash}\npoetry shell\n```\n\nInside the virtual environment you can access all the examples.\n\nInstalling dependencies\n-----------------------\n\nDependencies should be installed through pip or poetry, see below.\n\nUsing pip, you can use\n\n``` {.sourceCode .bash}\npip3 install \'.[options]\'\n```\n\nUsing poetry\n\n``` {.sourceCode .bash}\npoetry install --with <options>\n```\n\nOptions are `keyboard`.\n\nExamples\n--------\n\nYou find several python scripts in\n[examples/](https://github.com/maxspahn/gym_envs_urdf/tree/master/examples).\nYou can test those examples using the following (if you use poetry, make\nsure to enter the virtual environment first with `poetry shell`)\n\n``` {.sourceCode .python}\npython3 pointRobot.py\n```\n\nReplace pointRobot.py with the name of the script you want to run.\n',
    'author': 'Max Spahn',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': 'Max Spahn',
    'maintainer_email': 'm.spahn@tudelft.nl',
    'url': 'https://maxspahn.github.io/gym_envs_urdf/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
