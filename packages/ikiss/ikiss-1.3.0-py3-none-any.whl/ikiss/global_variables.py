from pathlib import Path
DOCS = "https://forge.ird.fr/diade/iKISS/-/blob/master/README.rst"
GIT_URL = "https://forge.ird.fr/diade/iKISS"

ALLOW_FASTQ_EXT = (".fastq", ".fq", ".fq.gz", ".fastq.gz")
ALLOW_MAPPING_MODE = ("bwa-aln", "bwa-mem2")

SINGULARITY_URL_FILES = [('https://itrop.ird.fr/ikiss_utilities/Singularity.ikiss_tools.sif',
              'INSTALL_PATH/containers/Singularity.ikiss_tools.sif')]

DATATEST_URL_FILES = ("https://itrop.ird.fr/ikiss_utilities/DATATEST.zip", "DATATEST.zip")