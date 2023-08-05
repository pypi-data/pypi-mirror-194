# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_extra', 'click_extra.tests']

package_data = \
{'': ['*']}

install_requires = \
['Pallets-Sphinx-Themes>=2.0.2,<3.0.0',
 'boltons>=23.0.0,<24.0.0',
 'click-log>=0.4.0,<0.5.0',
 'click>=8.1.1,<9.0.0',
 'cloup>=2.0.0.post1,<3.0.0',
 'commentjson>=0.9.0,<0.10.0',
 'mergedeep>=1.3.4,<2.0.0',
 'pygments-ansi-color>=0.0.6,<0.2.1',
 'pygments>=2.14.0,<3.0.0',
 'pyyaml>=6.0.0,<7.0.0',
 'regex>=2022.3.15,<2023.0.0',
 'requests>=2.27.1,<3.0.0',
 'sphinx>=5.3.0,<6.0.0',
 'tabulate[widechars]>=0.9.0,<0.10.0',
 'wcmatch>=8.4,<9.0',
 'xmltodict>=0.12,<0.14']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0'],
 ':python_version < "3.8"': ['importlib-metadata>=1.4']}

entry_points = \
{'pygments.filters': ['ansi-filter = click_extra.pygments:AnsiFilter'],
 'pygments.formatters': ['ansi-html-formatter = '
                         'click_extra.pygments:AnsiHtmlFormatter'],
 'pygments.lexers': ['ansi-bash-session = '
                     'click_extra.pygments:AnsiBashSessionLexer',
                     'ansi-dylan-console = '
                     'click_extra.pygments:AnsiDylanConsoleLexer',
                     'ansi-elixir-console = '
                     'click_extra.pygments:AnsiElixirConsoleLexer',
                     'ansi-erlang-shell = '
                     'click_extra.pygments:AnsiErlangShellLexer',
                     'ansi-gap-console = '
                     'click_extra.pygments:AnsiGAPConsoleLexer',
                     'ansi-julia-console = '
                     'click_extra.pygments:AnsiJuliaConsoleLexer',
                     'ansi-matlab-session = '
                     'click_extra.pygments:AnsiMatlabSessionLexer',
                     'ansi-msdos-session = '
                     'click_extra.pygments:AnsiMSDOSSessionLexer',
                     'ansi-output = click_extra.pygments:AnsiOutputLexer',
                     'ansi-postgres-console = '
                     'click_extra.pygments:AnsiPostgresConsoleLexer',
                     'ansi-power-shell-session = '
                     'click_extra.pygments:AnsiPowerShellSessionLexer',
                     'ansi-psysh-console = '
                     'click_extra.pygments:AnsiPsyshConsoleLexer',
                     'ansi-python-console = '
                     'click_extra.pygments:AnsiPythonConsoleLexer',
                     'ansi-r-console = click_extra.pygments:AnsiRConsoleLexer',
                     'ansi-ruby-console = '
                     'click_extra.pygments:AnsiRubyConsoleLexer',
                     'ansi-sqlite-console = '
                     'click_extra.pygments:AnsiSqliteConsoleLexer',
                     'ansi-tcsh-session = '
                     'click_extra.pygments:AnsiTcshSessionLexer'],
 'pygments.styles': ['ansi-click-extra-furo-style = '
                     'click_extra.pygments:AnsiClickExtraFuroStyle']}

setup_kwargs = {
    'name': 'click-extra',
    'version': '3.8.3',
    'description': '🌈 Extra colorization and configuration loading for Click.',
    'long_description': '<p align="center">\n  <a href="https://github.com/kdeldycke/click-extra/">\n    <img src="https://raw.githubusercontent.com/kdeldycke/click-extra/main/docs/images/logo-banner.svg" alt="Click Extra">\n  </a>\n</p>\n\n[![Last release](https://img.shields.io/pypi/v/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Python versions](https://img.shields.io/pypi/pyversions/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Unittests status](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml?query=branch%3Amain)\n[![Documentation status](https://github.com/kdeldycke/click-extra/actions/workflows/docs.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/click-extra/actions/workflows/docs.yaml?query=branch%3Amain)\n[![Coverage status](https://codecov.io/gh/kdeldycke/click-extra/branch/main/graph/badge.svg)](https://codecov.io/gh/kdeldycke/click-extra/branch/main)\n[![DOI](https://zenodo.org/badge/418402236.svg)](https://zenodo.org/badge/latestdoi/418402236)\n\n## What is Click Extra?\n\nA collection of helpers and utilities for\n[Click](https://click.palletsprojects.com), the Python CLI framework.\n\nIt is a drop-in replacement with good defaults that saves lots of boilerplate code and frustration.\nIt also comes with\n[workarounds and patches](https://kdeldycke.github.io/click-extra/issues.html) that have not\nreached upstream yet (or are unlikely to).\n\n## Example\n\nIt can transform this vanilla `click` CLI:\n\n![click CLI help screen](https://github.com/kdeldycke/click-extra/raw/main/docs/images/click-help-screen.png)\n\nInto this:\n\n![click-extra CLI help screen](https://github.com/kdeldycke/click-extra/raw/main/docs/images/click-extra-screen.png)\n\nTo undestrand how we ended up with the result above, go [read the tutorial](https://kdeldycke.github.io/click-extra/tutorial.html).\n\n## Features\n\n- Configuration file loader for:\n  - `TOML`\n  - `YAML`\n  - `JSON`, with inline and block comments (Python-style `#` and Javascript-style `//`)\n  - `INI`, with extended interpolation, multi-level sections and non-native types (`list`, `set`, …)\n  - `XML`\n- Download configuration from remote URLs\n- Optional strict validation of configuration\n- Search of configuration file from default user folder and glob patterns\n- Respect of `CLI` > `Configuration` > `Environment` > `Defaults` precedence\n- `--show-params` option to debug parameters defaults, values, environment variables and provenance\n- Colorization of help screens\n- `-h`/`--help` option names (see [rant on other inconsistencies](https://blog.craftyguy.net/cmdline-help/))\n- `--color`/`--no-color` option flag\n- Recognize the `NO_COLOR` environment variable convention from [`no-color.org`](https://no-color.org)\n- Colored `--version` option\n- Colored `--verbosity` option and logs\n- `--time`/`--no-time` flag to measure duration of command execution\n- Platform recognition utilities (macOS, Linux and Windows)\n- New conditional markers for `pytest`:\n  - `@skip_linux`, `@skip_macos` and `@skip_windows`\n  - `@unless_linux`, `@unless_macos` and `@unless_windows`\n  - `@destructive` and `@non_destructive`\n- [`.. click:example::` and `.. click:run::` Sphinx extensions](https://kdeldycke.github.io/click-extra/sphinx.html) to document CLI source code and their execution\n- [ANSI-capable Pygments lexers](https://kdeldycke.github.io/click-extra/pygments.html#lexers) for shell session and console output\n- Pygments styles and filters for ANSI rendering\n- [Fixes 30+ bugs](https://kdeldycke.github.io/click-extra/issues.html) from other Click-related projects\n- Rely on [`cloup`](https://github.com/janluke/cloup) to add:\n  - option groups\n  - constraints\n  - subcommands sections\n  - aliases\n  - command suggestion (`Did you mean <subcommand>?`)\n\n## Used in\n\nCheck these projects to get real-life examples of `click-extra` usage:\n\n- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/meta-package-manager?label=%E2%AD%90&style=flat-square) [Meta Package Manager](https://github.com/kdeldycke/meta-package-manager#readme)\n  \\- A unifying CLI for multiple package managers.\n- ![GitHub stars](https://img.shields.io/github/stars/kdeldycke/mail-deduplicate?label=%E2%AD%90&style=flat-square) [Mail Deduplicate](https://github.com/kdeldycke/mail-deduplicate#readme) - A\n  CLI to deduplicate similar emails.\n- ![GitHub stars](https://img.shields.io/github/stars/Sprocket-Security/fireproxng?label=%E2%AD%90&style=flat-square) [fireproxng](https://github.com/Sprocket-Security/fireproxng#readme) - A rewrite of the fireprox tool.\n- ![GitHub stars](https://img.shields.io/github/stars/hugolundin/badger?label=%E2%AD%90&style=flat-square) [badger-proxy](https://github.com/hugolundin/badger#readme) - An mDNS-based reverse\n  proxy for naming services on a local network.\n- ![GitHub stars](https://img.shields.io/github/stars/tclick/mdstab?label=%E2%AD%90&style=flat-square) [Molecular Dynamics Trajectory Analysis](https://github.com/tclick/mdstab#readme)\n\nFeel free to send a PR to add your project in this list if you are relying on Click Extra in any way.\n\n## Development\n\n[Development guidelines](https://kdeldycke.github.io/meta-package-manager/development.html)\nare the same as\n[parent project `mpm`](https://github.com/kdeldycke/meta-package-manager), from\nwhich `click-extra` originated.\n',
    'author': 'Kevin Deldycke',
    'author_email': 'kevin@deldycke.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kdeldycke/click-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
