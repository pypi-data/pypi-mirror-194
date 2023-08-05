# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vivlio']

package_data = \
{'': ['*'],
 'vivlio': ['Alert Settings/CSV/*',
            'Alert Settings/HTML/*',
            'Alert Settings/JSON/*',
            'Alert Settings/Markdown/*',
            'Alert Settings/Mindmap/*',
            'Alert Settings/YAML/*',
            'Clients/CSV/*',
            'Clients/HTML/*',
            'Clients/JSON/*',
            'Clients/Markdown/*',
            'Clients/Mindmap/*',
            'Clients/YAML/*',
            'Devices/CSV/*',
            'Devices/HTML/*',
            'Devices/JSON/*',
            'Devices/Markdown/*',
            'Devices/Mindmap/*',
            'Devices/YAML/*',
            'Management Interfaces/CSV/*',
            'Management Interfaces/HTML/*',
            'Management Interfaces/JSON/*',
            'Management Interfaces/Markdown/*',
            'Management Interfaces/Mindmap/*',
            'Management Interfaces/YAML/*',
            'Networks/CSV/*',
            'Networks/HTML/*',
            'Networks/JSON/*',
            'Networks/Markdown/*',
            'Networks/Mindmap/*',
            'Networks/YAML/*',
            'Organizations/CSV/*',
            'Organizations/HTML/*',
            'Organizations/JSON/*',
            'Organizations/Markdown/*',
            'Organizations/Mindmap/*',
            'Organizations/YAML/*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'meraki>=1.27.0,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'rich-click>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['vivlio = vivlio.script:run']}

setup_kwargs = {
    'name': 'vivlio',
    'version': '1.0.2',
    'description': 'Business ready documents from Meraki',
    'long_description': '# vivlio\n\nBusiness Ready Documents for Meraki\n\n## Current API Coverage\n\nAlert Settings\n\nOrganizations\n\nOrganization Devices\n\nOrganization Devices Management Interfaces\n\nOrganization Networks\n\nNetwork Clients\n\n## Installation\n\n```console\n$ python3 -m venv meraki\n$ source meraki/bin/activate\n(meraki) $ pip install vivlio\n```\n\n## Usage - Environment Variable - IMPORTANT\n\nPlease export / setup this environment variable prior to running vivlio\n\n```console\n(meraki) $ export MERAKI_DASHBOARD_API_KEY=<Meraki API Token>\n\n```\n\n## Usage - In-line\n\n```console\n(meraki) $ vivlio\n```\n\n## Recommended VS Code Extensions\n\nExcel Viewer - CSV Files\n\nMarkdown Preview - Markdown Files\n\nMarkmap - Mindmap Files\n\nOpen in Default Browser - HTML Files\n\n## Always On Sandbox\n\nThis code works with the always on sandbox! \n\nhttps://devnetsandbox.cisco.com/RM/Diagram/Index/a9487767-deef-4855-b3e3-880e7f39eadc?diagramType=Topology\n\n```console\nexport MERAKI_DASHBOARD_API_KEY=fd6dd87d96915f21bc0e0b3d96a866ff0e53e381\n\n(venv)$ pip install vivlio\n(venv)$ mkdir vivlio_output\n(venv)$ cd vivlio_output\n(venv)/vivlio_output$ vivlio\n(venv)/vivlio_output$ code . \n(Launches VS Code and you can view the output with the recommended VS Code extensions)\n```\n## Contact\n\nPlease contact John Capobianco if you need any assistance\n',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
