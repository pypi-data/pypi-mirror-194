# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiordr', 'aiordr.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'aiolimiter>=1.0.0,<2.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-socketio[asyncio-client]>=5.7.2,<6.0.0']

extras_require = \
{'docs': ['toml>=0.10.2,<0.11.0',
          'sphinx>=6.0.0,<7.0.0',
          'sphinx-rtd-theme>=1.1.1,<2.0.0'],
 'test': ['pytest>=7.2.0,<8.0.0',
          'pytest-asyncio>=0.20.2,<0.21.0',
          'pytest-mock>=3.10.0,<4.0.0',
          'toml>=0.10.2,<0.11.0',
          'types-toml>=0.10.8.1,<0.11.0.0']}

setup_kwargs = {
    'name': 'aiordr',
    'version': '0.0.3',
    'description': 'Simple and fast library for interacting with the o!rdr API.',
    'long_description': 'aiordr\n======\n\n|Python| |pypi| |pre-commit.ci status| |rtd| |pytest| |mypy| |codacy|\n\nSimple and fast asynchronous library for the o!rdr API.\n\n\nFeatures\n--------\n\n- Support for modern async syntax (async with)\n- Event decorators\n- Rate limit handling\n- Easy to use\n\n\nInstalling\n----------\n\n**Python 3.9 or higher is required**\n\nTo install the library, simply run the following commands\n\n.. code:: sh\n\n    # Linux/macOS\n    python3 -m pip install -U aiordr\n\n    # Windows\n    py -3 -m pip install -U aiordr\n\n\nTo install the development version, do the following:\n\n.. code:: sh\n\n    $ git clone https://github.com/NiceAesth/aiordr\n    $ cd aiordr\n    $ python3 -m pip install -U .\n\n\nAPI Example\n-----------\n\n.. code:: py\n\n    import aiordr\n    import asyncio\n\n\n    async def main():\n        client = aiordr.ordrClient(verification_key="verylongstring")\n\n        await client.create_render(\n            "username",\n            "YUGEN",\n            replay_url="https://url.to.replay",\n        )\n\n        @client.on_render_added\n        async def on_render_added(event: aiordr.models.RenderAddEvent) -> None:\n            print(event)\n\n        @client.on_render_progress\n        async def on_render_progress(event: aiordr.models.RenderProgressEvent) -> None:\n            print(event)\n\n        @client.on_render_fail\n        async def on_render_fail(event: aiordr.models.RenderFailEvent) -> None:\n            print(event)\n\n        @client.on_render_finish\n        async def on_render_finish(event: aiordr.models.RenderFinishEvent) -> None:\n            print(event)\n\n\n    if __name__ == "__main__":\n        asyncio.run(main())\n\n\nContributing\n------------\n\nPlease read the `CONTRIBUTING.rst <.github/CONTRIBUTING.rst>`__ to learn how to contribute to aiordr!\n\n\nAcknowledgments\n---------------\n\n-  `discord.py <https://github.com/Rapptz/discord.py>`__\n   for README formatting\n-  `aiosu <https://github.com/NiceAesth/aiosu>`__\n   sister library for the osu! API\n\n\n.. |Python| image:: https://img.shields.io/pypi/pyversions/aiordr.svg\n    :target: https://pypi.python.org/pypi/aiordr\n    :alt: Python version info\n.. |pypi| image:: https://img.shields.io/pypi/v/aiordr.svg\n    :target: https://pypi.python.org/pypi/aiordr\n    :alt: PyPI version info\n.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/NiceAesth/aiordr/master.svg\n    :target: https://results.pre-commit.ci/latest/github/NiceAesth/aiordr/master\n    :alt: pre-commit.ci status\n.. |pytest| image:: https://github.com/NiceAesth/aiordr/actions/workflows/pytest.yml/badge.svg\n    :target: https://github.com/NiceAesth/aiordr/actions/workflows/pytest.yml\n    :alt: pytest Status\n.. |mypy| image:: https://github.com/NiceAesth/aiordr/actions/workflows/mypy.yml/badge.svg\n    :target: https://github.com/NiceAesth/aiordr/actions/workflows/mypy.yml\n    :alt: mypy Status\n.. |rtd| image:: https://readthedocs.org/projects/aiordr/badge/?version=latest\n    :target: https://aiordr.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n.. |codacy| image:: https://app.codacy.com/project/badge/Grade/4778d5ee1dc84469ad6a43a6f961c0eb\n    :target: https://www.codacy.com/gh/NiceAesth/aiordr/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NiceAesth/aiordr&amp;utm_campaign=Badge_Grade\n    :alt: Codacy Status\n',
    'author': 'Nice Aesthetics',
    'author_email': 'nice@aesth.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NiceAesth/aiordr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
