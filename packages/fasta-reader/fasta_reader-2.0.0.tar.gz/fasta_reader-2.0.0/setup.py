# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fasta_reader']

package_data = \
{'': ['*']}

install_requires = \
['fsspec[github,http,s3,sftp]>=2023.1.0',
 'more-itertools>=9.1.0',
 'xopen>=1.7.0']

setup_kwargs = {
    'name': 'fasta-reader',
    'version': '2.0.0',
    'description': 'FASTA file reader/writer.',
    'long_description': '# Welcome to fasta-reader 👋\n\n> Read and write FASTA file\n\n### 🏠 [Homepage](https://github.com/EBI-Metagenomics/fasta-reader-py)\n\n## ⚡️ Requirements\n\n- Python >= 3.9\n\n## Install\n\n```sh\npip install fasta-reader\n```\n\n## Examples\n\nThe following example show that it can read a compressed file remotely seamlessly:\n\n```python\nfrom fasta_reader import read_fasta\n\nROOT = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/858/895"\nREF = "GCF_009858895.2_ASM985889v3"\nFILE = f"{ROOT}/{REF}/{REF}_genomic.fna.gz"\n\nprint("Severe acute respiratory syndrome coronavirus 2:")\nfor item in read_fasta(FILE):\n    print(item)\n```\n\nWe can also write a FASTA file in a compressed format directly:\n\n```python\nfrom fasta_reader import write_fasta\n\nwith write_fasta("protein.faa.gz") as file:\n    file.write_item("P01013 GENE X PROTEIN", "QIKDLLVSSSTDLDT...")\n```\n\n## 👤 Author\n\n- [Danilo Horta](https://github.com/horta)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n',
    'author': 'Danilo Horta',
    'author_email': 'fdanilo.horta@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/EBI-Metagenomics/fasta-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
