# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['epss_api']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=1.26.13,<2.0.0']

entry_points = \
{'console_scripts': ['push = tools.push:main',
                     'release = tools.release:main',
                     'sbom = tools.sbom:main',
                     'sphinx = tools.sphinx:main']}

setup_kwargs = {
    'name': 'epss-api',
    'version': '0.2.2',
    'description': 'EPSS API Python Client',
    'long_description': "=================\nEPSS API Client\n=================\n\n.. image:: https://badge.fury.io/py/epss-api.svg\n    :target: https://badge.fury.io/py/epss-api\n\n.. image:: https://img.shields.io/pypi/dw/epss-api?style=flat\n    :target: https://pypistats.org/packages/epss-api\n\n.. image:: https://github.com/kannkyo/epss-api/actions/workflows/python-ci.yml/badge.svg\n    :target: https://github.com/kannkyo/epss-api/actions/workflows/python-ci.yml\n\n.. image:: https://codecov.io/gh/kannkyo/epss-api/branch/main/graph/badge.svg?token=R40FT0KITO \n    :target: https://codecov.io/gh/kannkyo/epss-api\n\n.. image:: https://github.com/kannkyo/epss-api/actions/workflows/scorecards.yml/badge.svg\n    :target: https://github.com/kannkyo/epss-api/actions/workflows/scorecards.yml\n\nEPSS(Exploit Prediction Scoring System) API client.\n\nEPSS is the one of famous vulnerability score developed by FIRST (the Forum of Incident Response and Security Teams).\n\nEPSS's definition:\n\n    The Exploit Prediction Scoring System (EPSS) is an open, \n    data-driven effort for estimating the likelihood (probability) that a software vulnerability will be exploited in the wild. \n    Our goal is to assist network defenders to better prioritize vulnerability remediation efforts. \n    While other industry standards have been useful for capturing innate characteristics of a vulnerability and provide measures of severity, \n    they are limited in their ability to assess threat. \n    EPSS fills that gap because it uses current threat information from CVE and real-world exploit data. \n    The EPSS model produces a probability score between 0 and 1 (0 and 100%). \n    The higher the score, the greater the probability that a vulnerability will be exploited.\n\n    https://www.first.org/epss/\n\nThis package is most easiest and efficient EPSS api client.\n\nUsage\n=============\n\nEPSS has only 4 methods.\n\n.. code-block:: python\n\n    from epss_api import EPSS\n\n    client = EPSS()\n\n    value = client.scores\n    # value = [\n    #   {'cve': 'CVE-2022-39952', 'epss': '0.09029', 'percentile': '0.94031'},\n    #   {'cve': 'CVE-2023-0669', 'epss': '0.78437', 'percentile': '0.99452'},\n    #  ...\n    # ]\n\n    value = client.score(cve_id='CVE-2022-0669')\n    # value = {'epss': 0.0095, 'percentile': 0.32069}\n\n    value = client.epss(cve_id='CVE-2022-0669')\n    # value == 0.0095\n\n    value = client.percentile(cve_id='CVE-2022-0669')\n    # value == 0.32069\n\nIf you call either one method, EPSS client cache all CVE's score in memory.\nAfter caching, you can get all data very fast.\n",
    'author': 'kannkyo',
    'author_email': '15080890+kannkyo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kannkyo/epss-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
