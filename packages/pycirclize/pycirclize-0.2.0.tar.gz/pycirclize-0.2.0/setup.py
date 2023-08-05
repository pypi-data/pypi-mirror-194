# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycirclize', 'pycirclize.parser', 'pycirclize.utils']

package_data = \
{'': ['*'], 'pycirclize.utils': ['images/*']}

install_requires = \
['biopython>=1.79', 'matplotlib>=3.5.2', 'numpy>=1.21.1', 'pandas>=1.3.5']

setup_kwargs = {
    'name': 'pycirclize',
    'version': '0.2.0',
    'description': 'Circular visualization in Python',
    'long_description': '# pyCirclize: Circular visualization in Python\n\n![Python3](https://img.shields.io/badge/Language-Python3-steelblue)\n![OS](https://img.shields.io/badge/OS-_Windows_|_Mac_|_Linux-steelblue)\n![License](https://img.shields.io/badge/License-MIT-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/pycirclize.svg)](https://pypi.python.org/pypi/pycirclize)\n[![conda-forge](https://img.shields.io/conda/vn/conda-forge/pycirclize.svg?color=green)](https://anaconda.org/conda-forge/pycirclize)\n[![CI](https://github.com/moshi4/pyCirclize/actions/workflows/ci.yml/badge.svg)](https://github.com/moshi4/pyCirclize/actions/workflows/ci.yml)\n\n## Table of contents\n\n- [Overview](#overview)\n- [Installation](#installation)\n- [API Usage](#api-usage)\n- [Code Example](#code-example)\n- [Not Implemented Features](#not-implemented-features)\n\n## Overview\n\npyCirclize is a circular visualization python package implemented based on matplotlib.\nThis package is developed for the purpose of easily and beautifully plotting circular figure such as Circos Plot and Chord Diagram in Python.\nIn addition, useful genome and phylogenetic tree visualization methods for the bioinformatics field are also implemented.\npyCirclize was inspired by [circlize](https://github.com/jokergoo/circlize) and [pyCircos](https://github.com/ponnhide/pyCircos).\nMore detailed documentation is available [here](https://moshi4.github.io/pyCirclize/).\n\n![pyCirclize_gallery.png](https://raw.githubusercontent.com/moshi4/pyCirclize/main/docs/images/pyCirclize_gallery.png)  \n**Fig.1 pyCirclize example plot gallery**\n\n## Installation\n\n`Python 3.8 or later` is required for installation.\n\n**Install PyPI package:**\n\n    pip install pycirclize\n\n**Install conda-forge package:**\n\n    conda install -c conda-forge pycirclize\n\n## API Usage\n\nAPI usage is described in each of the following sections in the [document](https://moshi4.github.io/pyCirclize/).\n\n- [Getting Started](https://moshi4.github.io/pyCirclize/getting_started/)\n- [Plot API Example](https://moshi4.github.io/pyCirclize/plot_api_example/)\n- [Chord Diagram](https://moshi4.github.io/pyCirclize/chord_diagram/)\n- [Circos Plot (Genomics)](https://moshi4.github.io/pyCirclize/circos_plot/)\n- [Phylogenetic Tree](https://moshi4.github.io/pyCirclize/phylogenetic_tree/)\n\n## Code Example\n\n### 1. Circos Plot\n\n```python\nfrom pycirclize import Circos\nimport numpy as np\nnp.random.seed(0)\n\n# Initialize Circos sectors\nsectors = {"A": 10, "B": 15, "C": 12, "D": 20, "E": 15}\ncircos = Circos(sectors, space=5)\n\nfor sector in circos.sectors:\n    # Plot sector name\n    sector.text(f"Sector: {sector.name}", r=110, size=15)\n    # Create x positions & randomized y values\n    x = np.arange(sector.start, sector.end) + 0.5\n    y = np.random.randint(0, 100, len(x))\n    # Plot line track\n    line_track = sector.add_track((80, 100), r_pad_ratio=0.1)\n    line_track.xticks_by_interval(interval=1)\n    line_track.axis()\n    line_track.line(x, y)\n    # Plot points track\n    points_track = sector.add_track((55, 75), r_pad_ratio=0.1)\n    points_track.axis()\n    points_track.scatter(x, y)\n    # Plot bar track\n    bar_track = sector.add_track((30, 50), r_pad_ratio=0.1)\n    bar_track.axis()\n    bar_track.bar(x, y)\n\n# Plot links \ncircos.link(("A", 0, 3), ("B", 15, 12))\ncircos.link(("B", 0, 3), ("C", 7, 11), color="skyblue")\ncircos.link(("C", 2, 5), ("E", 15, 12), color="chocolate", direction=1)\ncircos.link(("D", 3, 5), ("D", 18, 15), color="lime", ec="black", lw=0.5, hatch="//", direction=2)\ncircos.link(("D", 8, 10), ("E", 2, 8), color="violet", ec="red", lw=1.0, ls="dashed")\n\ncircos.savefig("example01.png")\n```\n\n![example01.png](https://raw.githubusercontent.com/moshi4/pyCirclize/main/docs/images/example01.png)  \n\n### 2. Chord Diagram\n\n```python\nfrom pycirclize import Circos\nimport pandas as pd\n\n# Create matrix dataframe (3 x 6)\nrow_names = ["F1", "F2", "F3"]\ncol_names = ["T1", "T2", "T3", "T4", "T5", "T6"]\nmatrix_data = [\n    [10, 16, 7, 7, 10, 8],\n    [4, 9, 10, 12, 12, 7],\n    [17, 13, 7, 4, 20, 4],\n]\nmatrix_df = pd.DataFrame(matrix_data, index=row_names, columns=col_names)\n\n# Initialize Circos from matrix for plotting Chord Diagram\ncircos = Circos.initialize_from_matrix(\n    matrix_df,\n    space=5,\n    cmap="tab10",\n    label_kws=dict(size=12),\n    link_kws=dict(ec="black", lw=0.5, direction=1),\n)\n\ncircos.savefig("example02.png")\n```\n\n![example02.png](https://raw.githubusercontent.com/moshi4/pyCirclize/main/docs/images/example02.png)  \n\n## Not Implemented Features\n\nList of features implemented in other Circos plotting tools but not yet implemented in pyCirclize.\nI may implement them when I feel like it.\n\n- Plot histogram\n- Plot boxplot\n- Plot violin\n- Label position auto adjustment\n',
    'author': 'moshi4',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://moshi4.github.io/pyCirclize/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
