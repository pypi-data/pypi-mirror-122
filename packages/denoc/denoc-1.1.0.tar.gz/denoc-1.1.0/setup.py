# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['denoc']

package_data = \
{'': ['*']}

install_requires = \
['colores>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['denoc = denoc:main']}

setup_kwargs = {
    'name': 'denoc',
    'version': '1.1.0',
    'description': 'Utilities for compile JavaScript with Deno',
    'long_description': '# Denoc\n\n![CodeQL](https://github.com/UltiRequiem/denoc/workflows/CodeQL/badge.svg)\n![Pylint](https://github.com/UltiRequiem/denoc/workflows/Pylint/badge.svg)\n[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)\n[![PyPi Version](https://img.shields.io/pypi/v/denoc)](https://pypi.org/project/denoc)\n![Repo Size](https://img.shields.io/github/repo-size/ultirequiem/denoc?style=flat-square&label=Repo)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![Lines of Code](https://img.shields.io/tokei/lines/github.com/UltiRequiem/denoc?color=blue&label=Total%20Lines)\n\nCompile Deno executables and compress them for all platforms easily.\n\n## Install\n\nYou can install [denoc](https://pypi.org/project/denoc) from PyPI like any other package:\n\n```bash\npip install denoc\n```\n\nTo get the last version:\n\n```bash\npip install git+https:/github.com/UltiRequiem/denoc\n```\n\nIf you use Linux, you may need to install this with sudo to be able to access the command throughout your system.\n\n## Usage\n\nBasic usage:\n\n```bash\ndenoc compileMe.ts\n```\n\nThis will make a directory (`deno_builds`) with executables for all the supported platforms.\n\nOptional flags:\n\n```bash\ndenoc --outputDir deno_dir_output --compress True file.ts\n```\n\n- `outputDir`: The directory where the binaries will be, by default the directory is *deno_build*\n\n- `compress`: Compress the binaries directory\n\n### Usage Example\n\n- Build and Publish GitHub Action\n\n```yaml\nname: Compile\n\non:\n  push:\n    tags:\n      - "*"\n\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Checkout\n        uses: actions/checkout@v2\n\n      - uses: denoland/setup-deno@v1\n        with:\n          deno-version: v1.x\n\n      - name: Install denoc\n        run: pip install denoc\n\n      - name: Build for all platforms\n        run: denoc cli.ts\n\n      - name: Release\n        uses: softprops/action-gh-release@v1\n        with:\n          files: |\n            deno_builds/x86_64-unknown-linux-gnu\n            deno_builds/aarch64-apple-darwin \n            deno_builds/x86_64-apple-darwin\n            deno_builds/x86_64-pc-windows-msvc.exe\n          token: ${{ secrets.GITHUB_TOKEN }}\n```\n\n### License\n\n[This project](https://pypi.org/project/denoc) is licensed under the [MIT License](./LICENSE.md).\n',
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UltiRequiem/denoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
