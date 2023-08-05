# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gwas_sumstats_tools',
 'gwas_sumstats_tools.interfaces',
 'gwas_sumstats_tools.schema']

package_data = \
{'': ['*']}

install_requires = \
['hypothesis>=6.68.2,<7.0.0',
 'pandera[io]>=0.13.4,<0.14.0',
 'petl>=1.7.12,<2.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gwas-ssf = gwas_sumstats_tools.cli:app']}

setup_kwargs = {
    'name': 'gwas-sumstats-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': '# GWAS-SSF Tools\n\n\nA basic toolkit for reading and formatting GWAS sumstats files from the GWAS Catalog.\nBuilt with:\n* [Petl](https://petl.readthedocs.io/en/stable/index.html)\n* [Pydantic](https://docs.pydantic.dev/)\n* [Typer](https://typer.tiangolo.com/)\n\nThere are two commands, `read` and `format`.\n\n`read` is for:\n* Previewing a data file: _no options_\n* Extracting the field headers: `-h`\n* Extracting all the metadata: `-M`\n* Extacting specific field, value pairs from the metada: `-m <field name>` \n\n`format` is for:\n* Converting a minamally formatted sumstats data file to the standard format. This is not guaranteed to return a valid standard file, because manadatory data fields could be missing in the input. It simply does the following. `-s`\n  * Renames `variant_id` -> `rsid`\n  * Reorders the fields\n  * Converts `NA` missing values to `#NA`\n  * It is memory efficient and will take approx. 30s per 1 million records\n* Generate metadata for a data file: `-m`\n  * Read metadata in from existing file: `--meta-in <file>`\n  * Create metadata from the GWAS Catalog (internal use, requires authenticated API): `-g`\n  * Edit/add the values to the metadata: `-e` with `--<FIELD>=<VALUE>`\n\n\n##Usage\n\n```console\n$ gwas-ssf [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `format`: Format a sumstats file and...\n* `read`: Read a sumstats file\n\n### `gwas-ssf format`\n\nFormat a sumstats file and creating a new one. Add/edit metadata.\n\n**Usage**:\n\n```console\n$ gwas-ssf format [OPTIONS] FILENAME\n```\n\n**Arguments**:\n\n* `FILENAME`: Input sumstats file. Must be TSV or CSV and may be gzipped  [required]\n\n**Options**:\n\n* `-o, --ss-out PATH`: Output sumstats file\n* `-s, --minimal2standard`: Try to convert a valid, minimally formatted file to the standard format.This assumes the file at least has `p_value`  combined with rsid in `variant_id` field or `chromosome` and `base_pair_location`. Validity of the new file is not guaranteed because mandatory data could be missing from the original file.  [default: False]\n* `-m, --generate-metadata`: Create the metadata file  [default: False]\n* `--meta-out PATH`: Specify the metadata output file\n* `--meta-in PATH`: Specify a metadata file to read in\n* `-e, --meta-edit`: Enable metadata edit mode. Then provide params to edit in the `--<FIELD>=<VALUE>` format e.g. `--GWASID=GCST123456` to edit/add that value  [default: False]\n* `-g, --meta-gwas`: Populate metadata from GWAS Catalog  [default: False]\n* `-c, --custom-header-map`: Provide a custom header mapping using the `--<FROM>:<TO>` format e.g. `--chr:chromosome`  [default: False]\n* `--help`: Show this message and exit.\n\n### `gwas-ssf read`\n\nRead (preview) a sumstats file\n\n**Usage**:\n\n```console\n$ gwas-ssf read [OPTIONS] FILENAME\n```\n\n**Arguments**:\n\n* `FILENAME`: Input sumstats file  [required]\n\n**Options**:\n\n* `-h, --get-header`: Just return the headers of the file  [default: False]\n* `--meta-in PATH`: Specify a metadata file to read in, defaulting to <filename>-meta.yaml\n* `-M, --get-all-metadata`: Return all metadata  [default: False]\n* `-m, --get-metadata TEXT`: Get metadata for the specified fields e.g. `-m genomeAssembly -m isHarmonised\n* `--help`: Show this message and exit.\n\n\n## TODO:\n- [ ] Installation/distribution docs\n- [ ] Transformation features\n- [ ] update GWAS API',
    'author': 'jdhayhurst',
    'author_email': 'jhayhurst@ebi.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
