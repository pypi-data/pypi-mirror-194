# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datapane',
 'datapane._vendor',
 'datapane._vendor.munch',
 'datapane.app',
 'datapane.blocks',
 'datapane.client',
 'datapane.cloud_api',
 'datapane.common',
 'datapane.ipython',
 'datapane.legacy_apps',
 'datapane.legacy_runner',
 'datapane.processors',
 'datapane.resources',
 'datapane.resources.app_templates',
 'datapane.resources.app_templates.app',
 'datapane.resources.app_templates.hello',
 'datapane.resources.app_templates.report_py',
 'datapane.resources.html_templates',
 'datapane.resources.view_resources',
 'datapane.view']

package_data = \
{'': ['*'], 'datapane.resources.app_templates': ['report_ipynb/*']}

install_requires = \
['PyYAML>=5.4.0,<7.0.0',
 'altair>=4.0.0,<5.0.0',
 'base64io>=1.0.3,<2.0.0',
 'boltons>=20.0.0,<22.0.0',
 'chardet>=4.0.0,<6.0.0',
 'cheroot>=9.0.0,<10.0.0',
 'click-spinner>=0.1.8,<0.2.0',
 'click>=7.1.0,<9.0.0',
 'colorlog>=4.1.0,<7.0.0',
 'dacite>=1.0.2,<2.0.0',
 'datacommons-pandas>=0.0.3,<0.0.4',
 'datacommons>=1.4.3,<2.0.0',
 'dominate>=2.4.0,<3.0.0',
 'dulwich>=0.20.0,<0.22.0',
 'furl>=2.0.0,<3.0.0',
 'glom>=22.1.0,<24.0.0',
 'importlib_resources>=3.0.0,<6.0.0',
 'ipynbname>=2021.3.2,<2022.0.0',
 'jsonschema>=3.2.0,<5.0.0',
 'lxml>=4.0.0,<5.0.0',
 'micawber>=0.5.0',
 'multimethod>=1.9,<2.0',
 'nbconvert>=5.6.1',
 'packaging>=21.0.0,<24.0.0',
 'pandas>=1.1.0,<2.0.0',
 'posthog>=1.4.0,<3.0.0',
 'pyarrow>=6.0.0,<11.0.0',
 'pydantic>=1.6.0,<2.0.0',
 'pyngrok>=5.2.1,<6.0.0',
 'requests-toolbelt>=0.9.1,<0.11.0',
 'requests>=2.19.0,<3.0.0',
 'stringcase>=1.2.0,<2.0.0',
 'tabulate>=0.8.9,<0.10.0',
 'toolz>=0.11.0,<0.13.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'validators>=0.18.0,<0.21.0',
 'vega-datasets>=0.9.0,<1.0.0']

extras_require = \
{'cloud': ['flit-core>=3.1.0,<4.0.0'],
 'plotting': ['matplotlib>=3.2.0,<4.0.0',
              'plotly>=5.0.0,<6.0.0',
              'bokeh>=2.3.0,<3.0.0',
              'folium>=0.12.0,<0.15.0',
              'plotapi>=6.0.0,<7.0.0']}

entry_points = \
{'console_scripts': ['datapane = datapane.client.__main__:main',
                     'dp-runner = datapane.runner.__main__:main']}

setup_kwargs = {
    'name': 'datapane',
    'version': '0.16.0',
    'description': 'Datapane client library and CLI tool',
    'long_description': '<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://datapane-cdn.com/static/v1/datapane-logo-dark.svg.br" width="250px" alt="Datapane" />\n  </a>\n</p>\n<p align="center">\n  <a href="https://docs.datapane.com">Docs</a> |\n  <a href="https://datapane.com/cloud">Cloud</a> |\n <a href="https://forum.datapane.com">Discussions</a> |\n  <a href="https://chat.datapane.com">Discord</a>\n</p>\n<p align=\'center\'>\n  <a href="https://pypi.org/project/datapane/">\n      <img src="https://img.shields.io/pypi/dm/datapane?label=pip%20downloads" alt="Pip Downloads" />\n  </a>\n  <a href="https://pypi.org/project/datapane/">\n      <img src="https://img.shields.io/pypi/v/datapane?color=blue" alt="Latest release" />\n  </a>\n  <a href="https://anaconda.org/conda-forge/datapane">\n      <img alt="Conda (channel only)" src="https://img.shields.io/conda/vn/conda-forge/datapane">\n  </a>\n</p>\n\n<p align=\'center\'>\n  <h1 align=\'center\'>Build full-stack data analytics apps in Python</h1>\n</p>\nDatapane is an open-source framework for building robust, high-performance data apps from Python and Jupyter.\n<br><br>\n<br>\n<br>\n\n<p align="center">\n  <a href="https://datapane.com">\n    <img src="https://user-images.githubusercontent.com/3541695/176545400-919a327d-ddee-4755-b29f-bf85fbfdb4ef.png"  width=\'75%\'>\n  </a>\n</p>\n\n## Why use Datapane?\n\n#### **🚀 Not just for demos**\n\nBuild performant, robust full-stack apps which are simple to deploy and manage on any hosting platform. Add background processing, auth, and monitoring to go beyond MVPs.\n\n#### **📈 Share standalone reports with no server**\n\nExport static HTML reports which you can share on Slack or Email, with no backend required.\n\n#### **📙 Ship apps from Jupyter**\n\nBuild and ship data apps from inside your Jupyter Notebook and existing scripts in <5 lines of code.\n\n## Other Features\n\n- User sessions and state handling\n- Intelligent caching\n- Sub-5ms function response time\n- Easy integration with authentication/authorization\n- Integrate into existing web frameworks (like Flask or FastAPI)\n- Host on existing web-hosts, like Fly and Heroku\n- Background processing\n\n## How is Datapane\'s architecture unique?\n\nDatapane Apps use a combination of pre-rendered frontend elements and backend Python functions which are called on-demand. Result: low-latency apps which are simple to build, host, and scale.\n\n# Getting Started\n\nWant a head start? Check out our [Getting Started guide](TODO) to build a data science web app in 3m.\n\n## Installing Datapane\n\nThe best way to install Datapane is through pip or conda.\n\n#### pip\n\n```\n$ pip3 install -U datapane\n```\n\n#### conda\n\n```\n$ conda install -c conda-forge "datapane>=0.15.6"\n```\n\nDatapane also works well in hosted Jupyter environments such as Colab or Binder, where you can install as follows:\n\n```\n!pip3 install --quiet datapane\n```\n\n# Examples\n\n### 📊 Share plots, data, and more as reports\n\nCreate reports from pandas DataFrames, plots from your favorite libraries, and text.\n\n<p>\n\n<img width=\'485px\' align=\'left\' alt="Simple Datapane app example with text, plot and table" src="https://user-images.githubusercontent.com/3541695/176251650-f49ea9f8-3cd4-4eda-8e78-ccba77e8e02f.png">\n\n<p>\n\n```python\nimport altair as alt\nfrom vega_datasets import data\nimport datapane as dp\n\ndf = data.iris()\nfig = (\n    alt.Chart(df)\n    .mark_point()\n    .encode(\n        x="petalLength:Q",\n        y="petalWidth:Q",\n        color="species:N"\n    )\n)\nview = dp.Blocks(\n    dp.Plot(fig),\n    dp.DataTable(df)\n)\ndp.save_report(view, path="my_app.html")\n```\n\n</p>\n\n### 🎛 Layout using interactive blocks\n\nAdd dropdowns, selects, grid, pages, and 10+ other interactive blocks.\n\n<p>\n\n<img width=\'485px\' align=\'left\' alt="Complex layout" src="https://user-images.githubusercontent.com/3541695/176288321-44f7e76f-5032-434b-a3b0-ed7e3911b5d5.png">\n\n<p>\n\n```python\n...\n\nview = dp.Blocks(\n    dp.Formula("x^2 + y^2 = z^2"),\n    dp.Group(\n        dp.BigNumber(\n            heading="Number of percentage points",\n            value="84%",\n            change="2%",\n            is_upward_change=True\n        ),\n        dp.BigNumber(\n            heading="Simple Statistic", value=100\n        ), columns=2\n    ),\n    dp.Select(\n        dp.Plot(fig, label="Chart"),\n        dp.DataTable(df, label="Data")\n    ),\n)\ndp.save_report(view, path="layout_example.html")\n```\n\n### Add functions to create full-stack apps\n\nAdd forms which run backend functions, or refresh your app automatically to build dashboards. Serve locally or deploy to your favorite web-host.\n\n<p>\n\n<img width=\'485px\' align=\'left\' alt="Functions" src="https://user-images.githubusercontent.com/3541695/221241943-dc2a03ae-1fd9-4278-8636-6344c5098a5c.gif">\n\n<p>\n\n```python\nimport altair as alt\nfrom vega_datasets import data\nimport datapane as dp\n\ndf = data.iris()\n\ndef gen_assets(params):\n    subset = df[df[\'species\'] == params[\'species\']]\n\n    fig = alt.Chart(subset)\n            .mark_point()\n            .encode( x="petalLength:Q", y="petalWidth:Q")\n\n    return [dp.Plot(fig), dp.DataTable(subset)]\n\nview = dp.Form(\n    on_submit=gen_assets,\n    controls=dp.Controls(\n      species=dp.Choice(options=list(df[\'species\'].unique())\n    )\n)\n\ndp.serve_app(view)\n```\n\n# Get involved\n\n## Discord\n\nGet help from the team, share what you\'re building, and get to know others in the space!\n\n### 💬 [Join our discord server](https://chat.datapane.com)\n\n## Feedback\n\nLeave us some feedback, ask questions and request features.\n\n### 📮 [Give feedback](https://datapane.nolt.io)\n\n## Forums\n\nNeed technical help? Reach out on GitHub discussions.\n\n### 📜 [Ask a question](https://forum.datapane.com/)\n\n## Contribute\n\nLooking for ways to contribute to Datapane?\n\n### ✨ [Visit the contribution guide](https://github.com/datapane/datapane/blob/main/CONTRIBUTING.md).\n\n# Next Steps\n\n- [Join Discord](https://chat.datapane.com)\n- [Sign up for a free account](https://cloud.datapane.com/accounts/signup)\n- [Read the documentation](https://docs.datapane.com)\n- [Ask a question](https://forum.datapane.com/)\n\n## Analytics\n\nBy default, the Datapane Python library collects error reports and usage telemetry.\nThis is used by us to help make the product better and to fix bugs.\nIf you would like to disable this, simply create a file called `no_analytics` in your `datapane` config directory, e.g.\n\n### Linux\n\n```bash\n$ mkdir -p ~/.config/datapane && touch ~/.config/datapane/no_analytics\n```\n\n### macOS\n\n```bash\n$ mkdir -p ~/Library/Application\\ Support/datapane && touch ~/Library/Application\\ Support/datapane/no_analytics\n```\n\n### Windows (PowerShell)\n\n```powershell\nPS> mkdir ~/AppData/Roaming/datapane -ea 0\nPS> ni ~/AppData/Roaming/datapane/no_analytics -ea 0\n```\n\nYou may need to try `~/AppData/Local` instead of `~/AppData/Roaming` on certain Windows configurations depending on the type of your user-account.\n',
    'author': 'Datapane Team',
    'author_email': 'dev@datapane.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.datapane.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.12.0',
}


setup(**setup_kwargs)
