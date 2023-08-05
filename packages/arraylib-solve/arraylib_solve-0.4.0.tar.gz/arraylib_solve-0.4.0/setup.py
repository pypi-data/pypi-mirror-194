# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysudoku_package']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.79',
 'click>=8.1.3',
 'numba>=0.55.2',
 'numpy>=1.22.4',
 'pandas>=1.4.2',
 'pytest',
 'scikit-learn>=1.1.1',
 'scipy>=1.8.1']

entry_points = \
{'console_scripts': ['arraylib-deconvolve = pysudoku_package.main:deconvolve',
                     'arraylib-run = pysudoku_package.main:run']}

setup_kwargs = {
    'name': 'arraylib-solve',
    'version': '0.4.0',
    'description': 'Tool to computationally deconvolve combinatorially pooled arrayed random mutagenesis libraries',
    'long_description': '# arraylib-solve\n\n# Introduction\n\n`arraylib-solve` is a tool to deconvolve combinatorially pooled arrayed random mutagenesis libraries (e.g. by transposon mutagenesis). In a typical experiment generating arrayed mutagenesis libraries, first a pooled version of the library is created and arrayed on a grid of well plates. To infer the identities of each mutant on the well plate, wells are pooled in combinatorial manner such that each mutant appears in a unique combination of pools. The pools are then sequenced using NGS and sequenced reads are stored in individual fastq files per pool. `arraylib-solve` deconvolves the pools and returns summaries stating the identity and location of each mutant on the original well grid. The package is based on the approach described in [[1]](#1).\n\n# Installation\n\nTo install `arraylib-solve` first create `Python 3.8` environment e.g. by\n\n```\nconda create --name arraylib-env python=3.8\nconda activate arraylib-env\n```\n\nand install the package using \n\n```\npip install arraylib-solve\n```\n\n\n# How to run `arraylib-solve`\n\nTo run `arraylib-solve` on a library deconvolution experiment with default parameters run:\n\n```\narraylib-run <input_directory> <experimental_design.csv> -b <path_to_genbank_reference> -br <path_to_bowtie2_indices> -t <transposon_sequence> -bu <upstream_sequence_of_barcodes> -bd <downstream_sequence_of_barcodes>\n```\n\n## Input parameters\n\nRequired parameters:\n* input_dir: path to directory holding the input fastq files\n* exp_design: path to file indicating experimental design. The experimental design file \n       should have columns, Filename, Poolname and Pooldimension. (see example in tests/test_data/full_exp_design.csv)\n       - Filename should contain all the unqiue input fastq filenames.\n       - Poolname should indicate to which pool a given file belongs. Multiple files per poolname are allowed.\n       - Pooldimension indicates the pooling dimension a pool belongs to. All pools sharing the same pooling dimension should have the same string in the Pooldimension column. \n* -gb path to genbank reference file\n* -br path to bowtie index files, ending with the basename of your index (if the basename of your index is UTI89 and you store your bowtie2 references in bowtie_ref it should be bowtie_ref/UTI89). Please visit https://bowtie-bio.sourceforge.net/bowtie2/manual.shtml#the-bowtie2-build-indexer for a manual how to create bowtie2 indices.\n* -t transposon sequence (e.g. ATTGCCTA)\n* -bu upstream sequence of barcode\n* -bd downstream sequence of barcode\n\nOptional parameters:\n* -mq minimum bowtie2 alignment quality score for each base to include read\n* -sq minimum phred score for each base to include read\n* -tm number of transposon mismatches allowed\n* -thr threshold for local filter (e.g. a threshold of 0.05 would filter out all reads < 0.05 of the maximum read count for a given mutant)\n\n## Output\n\n`arraylib-solve` outputs 4 files: \n* count_matrix.csv: Read counts per pool for each mutant.\n* filtered_matrix.csv: Read counts per pool for each mutant, but mutants with barcodes with low read counts for a given genomic location are filtered out.\n* mutant_location_summary.csv: A summary of mutants found in the well plate grid, where each row corresponds to a different mutant.\n* well_location_summary.csv: A summary of the deconvolved well plate grid, where each row corresponds to a different well.\n\n\n\n# References\n<a id="1">[1]</a> \nBaym, M., Shaket, L., Anzai, I.A., Adesina, O. and Barstow, B., 2016. Rapid construction of a whole-genome transposon insertion collection for Shewanella oneidensis by Knockout Sudoku. Nature communications, 7(1), p.13270.\n\n',
    'author': 'capraz',
    'author_email': 'tuemayc@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
