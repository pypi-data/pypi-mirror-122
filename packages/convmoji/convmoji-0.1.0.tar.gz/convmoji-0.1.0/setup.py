# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convmoji']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['convmoji = convmoji.commit:app']}

setup_kwargs = {
    'name': 'convmoji',
    'version': '0.1.0',
    'description': 'A simple cli tool to commit Conventional Commits with emojis.',
    'long_description': '\n[![Test](https://github.com/KnowKit/convmoji/actions/workflows/test.yaml/badge.svg)](https://github.com/KnowKit/convmoji/actions/workflows/test.yaml)\n[![codecov](https://codecov.io/gh/KnowKit/convmoji/branch/main/graph/badge.svg?token=84LAM4S1RD)](https://codecov.io/gh/KnowKit/convmoji)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n# convmoji\n\nA simple cli tool to commit Conventional Commits.\n\n## usage\n\n````bash\nconvmoji commit feature "my commit message"\nconvmoji commit feature devscope "my commit message"\nconvmoji commit feature devscope "my commit message" \\\n  --ammend --no-verify\nconvmoji commit feature devscope "my commit message" --body "my body message" \\\n  --footer "my body message" \\\n  --breacking-change "contains a breaking change" \\\n  --ammend --no-verify\n\n# If you want to see what to does without performing the action, run it with --debug\nconvmoji commit feature devscope "my commit message" <MoreOptions> --debug\n````\n\n## commit types\n\n* `feat`: ✨\n* `fix`: 🐛\n* `docs`: 📚\n* `style`: 💎\n* `refactor`: 🔨\n* `perf`: 🚀\n* `test`: 🚨\n* `build`: 📦\n* `ci`: 👷\n* `chore`: 🔧',
    'author': 'arrrrrmin',
    'author_email': 'info@dotarmin.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
