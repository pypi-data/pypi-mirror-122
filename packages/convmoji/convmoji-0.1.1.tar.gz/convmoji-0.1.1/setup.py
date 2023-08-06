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
    'version': '0.1.1',
    'description': 'A simple cli tool to commit Conventional Commits with emojis.',
    'long_description': '\n[![Build](https://github.com/KnowKit/convmoji/actions/workflows/build.yaml/badge.svg)](https://github.com/KnowKit/convmoji/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/KnowKit/convmoji/branch/main/graph/badge.svg?token=84LAM4S1RD)](https://codecov.io/gh/KnowKit/convmoji)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n# convmoji\n\nA simple cli tool to commit Conventional Commits.\n\n### Install\n\n```bash\npip install convmoji\nconvmoji --help\n```\n\n## Usage\n\n```\nconvmoji --help\n\nUsage: convmoji [OPTIONS] DESCRIPTION COMMIT_TYPE [SCOPE] [BODY] [FOOTER]\n\nArguments:\n  DESCRIPTION  Commit message, as in \'git commit -m "..."\'  [required]\n  COMMIT_TYPE  Either of feat fix docs style refactor perf test build ci chore\n               [required]\n  [SCOPE]      Scope for commit (any string)  [default: ]\n  [BODY]       Body message for commit  [default: ]\n  [FOOTER]     Footer message (formatted two blank lines below body)\n               [default: ]\n\nOptions:\n  --breaking-changes TEXT         Specially formatted message to show changes\n                                  might break previous versions\n  -a, --amend                     Execute commit with --amend\n  --no-verify, --nv               Execute commit with --no-verify\n  --co-authored_by, --co TEXT     A string of authors formatted like:\n                                  --co-authored-by \'<User user@no-reply> \'\n                                  --co-authored-by \'<User2 user2@no-reply>\'\n  --debug / --no-debug            [default: no-debug]\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n\n## Examples\n\nA conventianal commit\n````bash\nconvmoji "epic feature added" feat\n````\n\nOne with a scope\n````bash\nconvmoji "epic feature added" feat somescope\n# ✨: epic feature added\n````\n\nWith some options\n````bash\nconvmoji "epic feature added" feat somescope --amend --no-verify\n# ✨(somescope): epic feature added --amend --no-verify\n````\n\nWith more textual information\n````bash\nconvmoji "epic feature added" feat somescope \\\n  "more body information" "more footer information"\n# ✨(somescope): epic feature added\n# \n# more body information\n# \n# more footer information\n````\n\nInform people about breaking changes\n````bash\nconvmoji "epic feature added" feat somescope \\ \n  "more body information" "more footer information" \\\n  --breaking-changes "breaks somthing"\n# ✨‼️(somescope): epic feature added\n# \n# more body information\n# \n# BREAKING CHANGE: breaks somthing\n# more footer information\n````\n\n> If you want to see what to does without performing the action, run it with `--debug`\n\n## Commit types\n\nFor details on commit types see [conventional commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).\n\n* `feat`: ✨\n* `fix`: 🐛\n* `docs`: 📚\n* `style`: 💎\n* `refactor`: 🔨\n* `perf`: 🚀\n* `test`: 🚨\n* `build`: 📦\n* `ci`: 👷\n* `chore`: 🔧',
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
