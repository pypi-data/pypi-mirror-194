# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pymsaviz', 'pymsaviz.config', 'pymsaviz.scripts']

package_data = \
{'': ['*'], 'pymsaviz.config': ['testdata/*']}

install_requires = \
['biopython>=1.79', 'matplotlib>=3.5.2']

entry_points = \
{'console_scripts': ['pymsaviz = pymsaviz.scripts.cli:main']}

setup_kwargs = {
    'name': 'pymsaviz',
    'version': '0.3.0',
    'description': 'MSA visualization python package for sequence analysis',
    'long_description': '# pyMSAviz\n\n![Python3](https://img.shields.io/badge/Language-Python3-steelblue)\n![OS](https://img.shields.io/badge/OS-_Windows_|_Mac_|_Linux-steelblue)\n![License](https://img.shields.io/badge/License-MIT-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/pymsaviz.svg)](https://pypi.python.org/pypi/pymsaviz)\n[![Bioconda](https://img.shields.io/conda/vn/bioconda/pymsaviz.svg?color=green)](https://anaconda.org/bioconda/pymsaviz)\n[![CI](https://github.com/moshi4/pyMSAviz/actions/workflows/ci.yml/badge.svg)](https://github.com/moshi4/pyMSAviz/actions/workflows/ci.yml)\n\n## Table of contents\n\n- [Overview](#overview)\n- [Installation](#installation)\n- [API Usage](#api-usage)\n- [CLI Usage](#cli-usage)\n\n## Overview\n\npyMSAviz is a MSA(Multiple Sequence Alignment) visualization python package for sequence analysis implemented based on matplotlib.\nThis package is developed for the purpose of easily and beautifully plotting MSA in Python.\nIt also implements the functionality to add markers, text annotations, highlights to specific positions and ranges in MSA.\npyMSAviz was developed inspired by [Jalview](https://www.jalview.org/) and [ggmsa](https://github.com/YuLab-SMU/ggmsa).\nMore detailed documentation is available [here](https://moshi4.github.io/pyMSAviz/).\n\n![example01.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/api_example01.png)  \n**Fig.1 Simple visualization result**\n\n![example03.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/api_example03.png)  \n**Fig.2 Customized visualization result**\n\n## Installation\n\n`Python 3.8 or later` is required for installation.\n\n**Install PyPI package:**\n\n    pip install pymsaviz\n\n**Install bioconda package:**\n\n    conda install -c conda-forge -c bioconda pymsaviz\n\n## API Usage\n\nOnly simple example usage is described in this section.\nFor more details, please see [Getting Started](https://moshi4.github.io/pyMSAviz/getting_started/) and [API Docs](https://moshi4.github.io/pyMSAviz/api-docs/msaviz/).\n\n### API Example\n\n#### API Example 1\n\n```python\nfrom pymsaviz import MsaViz, get_msa_testdata\n\nmsa_file = get_msa_testdata("HIGD2A.fa")\nmv = MsaViz(msa_file, wrap_length=60, show_count=True)\nmv.savefig("api_example01.png")\n```\n\n![example01.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/api_example01.png)  \n\n#### API Example 2\n\n```python\nfrom pymsaviz import MsaViz, get_msa_testdata\n\nmsa_file = get_msa_testdata("MRGPRG.fa")\nmv = MsaViz(msa_file, color_scheme="Taylor", wrap_length=80, show_grid=True, show_consensus=True)\nmv.savefig("api_example02.png")\n```\n\n![example02.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/api_example02.png)  \n\n#### API Example 3\n\n```python\nfrom pymsaviz import MsaViz, get_msa_testdata\n\nmsa_file = get_msa_testdata("MRGPRG.fa")\nmv = MsaViz(msa_file, end=180, wrap_length=60, show_consensus=True)\n\n# Extract MSA positions less than 50% consensus identity\npos_ident_less_than_50 = []\nident_list = mv._get_consensus_identity_list()\nfor pos, ident in enumerate(ident_list, 1):\n    if ident <= 50:\n        pos_ident_less_than_50.append(pos)\n\n# Add markers\nmv.add_markers([1])\nmv.add_markers([10, 20], color="orange", marker="o")\nmv.add_markers([30, (40, 50), 55], color="green", marker="+")\nmv.add_markers(pos_ident_less_than_50, marker="x", color="blue")\n# Add text annotations\nmv.add_text_annotation((76, 102), "Gap Region", text_color="red", range_color="red")\nmv.add_text_annotation((112, 123), "Gap Region", text_color="green", range_color="green")\n\nmv.savefig("api_example03.png")\n```\n\n![example03.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/api_example03.png)  \n\n## CLI Usage\n\npyMSAviz provides simple MSA visualization CLI.\n\n### Basic Command\n\n    pymsaviz -i [MSA file] -o [MSA visualization file]\n\n### Options\n\n    -i I, --infile I    Input MSA file\n    -o O, --outfile O   Output MSA visualization file (*.png|*.jpg|*.svg|*.pdf)\n    --format            MSA file format (Default: \'fasta\')\n    --color_scheme      Color scheme (Default: \'Zappo\')\n    --start             Start position of MSA visualization (Default: 1)\n    --end               End position of MSA visualization (Default: \'MSA Length\')\n    --wrap_length       Wrap length (Default: None)\n    --wrap_space_size   Space size between wrap MSA plot area (Default: 3.0)\n    --show_grid         Show grid (Default: OFF)\n    --show_count        Show seq char count without gap on right side (Default: OFF)\n    --show_consensus    Show consensus sequence (Default: OFF)\n    --consensus_color   Consensus identity bar color (Default: \'#1f77b4\')\n    --consensus_size    Consensus identity bar height size (Default: 2.0)\n    --sort              Sort MSA order by NJ tree constructed from MSA distance matrix (Default: OFF)\n    --dpi               Figure DPI (Default: 300)\n    -v, --version       Print version information\n    -h, --help          Show this help message and exit\n\n    Available Color Schemes:\n    [\'Clustal\', \'Zappo\', \'Taylor\', \'Flower\', \'Blossom\', \'Sunset\', \'Ocean\', \'Hydrophobicity\', \'HelixPropensity\', \n     \'StrandPropensity\', \'TurnPropensity\', \'BuriedIndex\', \'Nucleotide\', \'Purine/Pyrimidine\', \'Identity\', \'None\']\n\n### CLI Example\n\nClick [here](https://github.com/moshi4/pyMSAviz/raw/main/example/example.zip) to download example MSA files.  \n\n#### CLI Example 1\n\n    pymsaviz -i ./example/HIGD2A.fa -o cli_example01.png --color_scheme Identity\n\n![example01.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/cli_example01.png)  \n\n#### CLI Example 2\n\n    pymsaviz -i ./example/MRGPRG.fa -o cli_example02.png --wrap_length 80 \\\n             --color_scheme Taylor --show_consensus --show_count\n\n![example02.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/cli_example02.png)  \n\n#### CLI Example 3\n\n    pymsaviz -i ./example/MRGPRG.fa -o cli_example03.png --start 100 --end 160 \\\n             --color_scheme Flower --show_grid --show_consensus --consensus_color tomato \n\n![example03.png](https://raw.githubusercontent.com/moshi4/pyMSAviz/main/docs/images/cli_example03.png)  \n',
    'author': 'moshi4',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://moshi4.github.io/pyMSAviz/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
