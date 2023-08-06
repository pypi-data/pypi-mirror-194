# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mosum']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0', 'numpy>=1.24.1,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'mosum',
    'version': '0.1.0',
    'description': 'Moving Sum Based Procedures for Changes in the Mean',
    'long_description': '# mosum.py: Moving Sum Based Procedures for Changes in the Mean\n\nA python port of the R package mosum <https://CRAN.R-project.org/package=mosum>.\nImplementations of MOSUM-based statistical procedures and algorithms for detecting multiple changes in the mean. \nThis comprises the MOSUM procedure for estimating multiple mean changes from Eichinger and Kirch (2018) <doi:10.3150/16-BEJ887> \nand the multiscale algorithmic extension from Cho and Kirch (2022) <doi:10.1007/s10463-021-00811-5>, \nas well as the bootstrap procedure for generating confidence intervals about the locations of change points as proposed in Cho and Kirch (2022) <doi:10.1016/j.csda.2022.107552>. \nSee also Meier, Kirch and Cho (2021) <doi:10.18637/jss.v097.i08> which accompanies the R package.\n\n## Installation\n\n```bash\n$ pip install mosum\n```\n\n## Usage\n\nmosum.py can be used as follows to detect changes in the mean of a time series\n\n```python\nimport mosum\n#   simulate data\nxx = mosum.testData("blocks")["x"]\n# detect changes\nxx_m  = mosum.mosum(xx, G = 50, criterion = "eta", boundary_extension = True)\n# summary and print methods\nxx_m.summary()\nxx_m.print()\n# plot the output\nxx_m.plot(display="mosum")\nfrom matplotlib import pyplot as plt\nplt.show()\n```\n\n## License\n\nmosum.py was created by Dom Owens, based on the R package "mosum", originally by Alexander Meier, Haeran Cho, and Claudia Kirch.\nIt is licensed under the terms of the MIT license.',
    'author': 'Dom Owens',
    'author_email': 'dom.owens@bristol.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
