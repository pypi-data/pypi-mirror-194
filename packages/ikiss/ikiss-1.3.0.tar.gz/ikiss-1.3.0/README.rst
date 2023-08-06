.. image:: ./ikiss/logo_ikiss.png
   :width: 400
   :alt: ikiss Logo
   :align: center


|PythonVersions| |SnakemakeVersions| |Singularity|

.. contents:: Table of Contents
    :depth: 2


**Homepage:** https://forge.ird.fr/diade/iKISS

About iKISS 
===============

**iKISS (Kmer Inference sSelection)** is a snakemake pipeline able to decompose reads into kmers and extract kmers under selection. 

iKISS uses KmersGWAS https://github.com/voichek/kmersGWAS, pcadapt https://cran.r-project.org/web/packages/pcadapt/readme/README.html and lfmm https://bcm-uga.github.io/lfmm/articles/lfmm to select genomics regions under selection.

1. Install dependencies and clone iKISS
=============================================

Check dependencies for iKISS : python and singularity

Install  singularity and python3 in your local machine OR use module load to add singularity and python3 in your environment if you are working in a cluster :

.. code-block:: bash

   module load system/python/3.8.12
   module load system/singularity/3.6.0


iKISS is NOW available as a PyPI package (recommended)

.. code-block:: bash

   python3 -m pip install ikiss


OR you can also install iKISS from git repository

.. code-block:: bash

   python3 -m pip install ikiss@git+https://forge.ird.fr/diade/iKISS.git 
   
   #OR
   
   git clone https://forge.ird.fr/diade/iKISS.git 
   cd iKISS
   python3 -m pip install .


1.1 Installing in cluster mode
-------------------------------

Install iKISS in cluster mode using **singularity** container from ikiss_utilities https://itrop.ird.fr/ikiss_utilities/

.. code-block:: bash

   ikiss install_cluster --help
   ikiss install_cluster --scheduler slurm --env singularity
   

1.2 Installing in local mode 
----------------------------

.. code-block:: bash

   ikiss install_local --help
   ikiss install_local


2. Running a datatest
=============================================

Running test with a datatest from iKISS_utilities in a repertory TEST

.. code-block:: bash

   ikiss test_install --help
   ikiss test_install -d TEST


2.1 In CLUSTER mode
-------------------

Launching suggested command line done by iKISS, in CLUSTER mode : 

Please run command line 'ikiss create_cluster_config' before the first run and modify theads, ram, node and computer ressources. 
iKISS do a copy of cluster_config.yaml file into your home "/home/$USER/.config/ikiss/cluster_config.yaml"

   
.. code-block:: bash

   ikiss run_cluster --help
   ikiss create_cluster_config

If singularity was selected in installation of iKISS, it could be needed to give argument --singularity-args \"--bind $HOME\" to Snakemake, by using :

.. code-block:: bash

   ikiss run_cluster --help
   ikiss run_cluster -c TEST/data_test_config.yaml --singularity-args "--bind $HOME"
   # @IFB
   ikiss run_cluster -c TEST/data_test_config.yaml --singularity-args "--bind /shared:/shared"


**Important Note** : In i-Trop cluster, run iKISS using ONLY a node, data has to be in "/scratch" of chosen node. Use `nodelist : nodeX` parametter inside of cluster_config.yaml file.


2.2 In LOCAL mode
-----------------

launching suggested command line done by iKISS, in LOCAL mode: 

.. code-block:: bash

   ikiss run_local --help
   ikiss run_local -t 8 -c TEST/data_test_config.yaml --singularity-args "--bind $HOME"

In local mode, its possible to allocate threads to some rules using `--set-threads` snakemake argument such as

.. code-block:: bash

    ikiss run_local -t 8 -c TEST/data_test_config.yaml --set-threads kmers_gwas_per_sample=4 mapping_kmers=2 filter_bam=2 kmer_position_from_bam=4 pcadapt=2 extract_kmers_from_bed=2


3. Running your data
========================


3.1. Adapt config.yaml
------------------------

Before to run iKISS, adapt `config.yaml` by using : 

.. code-block:: bash

   ikiss create_config


Adapt `config.yaml` file with path to fastq files (FASTQ) and outfile (OUTPUT) in the `DATA` section. 

.. code-block:: yaml

   DATA:
      FASTQ: './DATATEST/fastq'
      OUTPUT: './OUTPUT-KISS/'

:warning if yours reads are ilumina paired, you need rename reads SAMPLE_R1.fastq.gz and SAMPLE_R2.fastq.gz. For single reads use SAMPLE_R1.fastq.gz

iKISS uses compressed ans decompressed fastq files.


3.1.1 WORKFLOW section
-----------------------

Parameter iKISS steps using the section WORKFLOW and parameter it with the PARAMS sections.

In WORKFLOW section:

   KMERS_GWAS step has to be activated by default. 

   PCADAPT, LFMM, MAPPING or ASSEMBLY are optional. Active or deactivate these steps using true or false.


**KMERS_GWAS** convert reads in kmers, filter them and create a format ready to use in population genomics!

**PCADAPT** detects genetic markers (kmers here ^^) involved in biological adaptation and provides outlier detection based on Principal Component Analysis (PCA).

**LFMM** is used by iKISS for testing correlations between kmers and environmental data.

**MAPPING** can optionally be used to align kmers to a genomic reference (if it is available ! ).

**ASSEMBLY** can optionally assembly significant kmers obtained by pcadapt or lfmm

.. code-block:: yaml

   WORKFLOW:
      KMERS_MODULE : true
      PCADAPT : true
      LFMM : true
      MAPPING: true
      ASSEMBLY: true

3.1.2 PARAMS section
--------------------

In the PARAMS section, tools parameters can be modified and adapted.


=> 1. KMERS_MODULE
-------------------

KMERS_GWAS module decompose reads into kmers and create a binary table of presence/absence of kmers. This table can be filter to use only most informative kmers into the populations. PLINK format outfiles are obtained in this module.

.. code-block:: yaml

   PARAMS:
      KMERS_MODULE:
         KMER_SIZE : 31
         MAC : 2
         P : 0.2
         MAF : 0.05
         B : 1000000 # nb kmers in each bed file
         SPLIT_LIST_SIZE : 100000
         MIN_LIST_SIZE : 50000


**KMER_SIZE** is the length of kmers (should be between 15-31)

**MAC** is the minor allele count (min allowed appearance of a kmer) 

**P** is the minimum percent of appearance in each strand form

**MAF** is the minimum allele frequency

**B** is the number of kmers in each bed file

**SPLIT_LIST_SIZE** is the nb of kmers by bed file

**MIN_LIST_SIZE** indicates the minimal number of kmers allowed in the smaller bed file after splitting


=> 2. PCADAPT
--------------

PCADAPT detects kmers involved in biological adaptation and provides outlier detection based on Principal Component Analysis (PCA)

.. code-block:: yaml

   PARAMS:        
      PCADAPT:
         K : 2
         SAMPLES: "samples.txt"
         CORRECTION: 'FDR'
         ALPHA : 0.05


**K** : number K of principal components

**SAMPLES** : you need to generate a *samples.txt* file.  This file contains two columns (tab delimitations) : accession_id and phenotype_value. It will be used by PCADAPT.

   **accession_id** : contains exactly same name of samples in FASTQ. 

   **phenotype_value** (int): contains sample group (wild=1, cultivated=2 for example)

.. code-block:: bash

   accession_id	phenotype_value
   Clone12	2
   Clone14	2
   Clone16	2
   Clone20	2
   Clone2	1
   Clone4	1
   Clone8	1

**CORRECTION**: kmers outliers are obtained using a correction of BONFERONNI, BH or FDR model.

**ALPHA**: modify the alpha cutoff for outlier detection


=> 3. LFMM
----------

LFMM is used by iKISS for testing correlations between kmers and environmental data.

.. code-block:: yaml

   PARAMS:
      LFMM:
         K : 2
         PHENOTYPE_FILE: "pheno.txt"
         PHENOTYPE_PCA_ANALYSIS : false
         CORRECTION: 'BH'
         ALPHA : 0.05


**K** are the latent factors used in LFMM association analyses 

**PHENOTYPE_FILE**: an phenotype file is obligatory in LFMM analysis. You can give to iKISS PCA results, climate variables, etc.

A PCA can reveal some 'structure' in the genotype data and it could help you to fix K parameter.

**PHENOTYPE_PCA_ANALYSIS** 

   * If **PHENOTYPE_PCA_ANALYSIS** is true, iKISS automatically run PCA using the file given by user in the PHENOTYPE_FILE key. This PHENOTYPE_FILE can be a PCA result for example.

   * If **PHENOTYPE_PCA_ANALYSIS** is false, iKISS use directly the PHENOTYPE_FILE as 'phenotype' to LFMM analysis. Kmers are used as 'genotype' data. 

**CORRECTION**: kmers outliers are obtained using a correction of BONFERONNI, BH or FDR model.

**ALPHA**: modify the alpha cutoff for outlier detection


=> 4. MAPPING
-------------

MAPPING section in PARAMS can optionally be used to align kmers to a genomic reference. It could give a idea of selected regions in a genome. 

.. code-block:: yaml

   PARAMS:
      MAPPING:
         REF: "reference.fasta"
         MODE : bwa-aln
         INDEX_OPTIONS: ""
         OPTIONS : "-n 0.04"


Use a reference file in the **REF** section. 

Parametter **MODE** using  *bwa-aln* or *bwa-mem2* 

Set up the **INDEX_OPTIONS** according to the MODE you have chosen.

   If *bwa-mem2* leaf empty
   
   If *bwa-aln* "-a bwtsw" or "" 

Set options according of chosen mapper in the **OPTIONS** key. 

   If *bwa-mem2* default parameters -A 1 -B 4;
   
   If *bwa-aln* -n 0.04

=> 5. ASSEMBLY
---------------

ASSEMBLY section in PARAMS can optionally be used to assembly significant kmers obtained by pcadapt or/and lfmm.

Contigs are assembled by iKISS using  mergeTags from dekupl package https://github.com/Transipedia/dekupl-mergeTags.

Chose minimal overlap size "OVERLAP_SIZE" allowed to assembly kmers.

Feel free to filter contigs by size "FILTER_CONTIG_SIZE".

Assembled contigs could be used by blastn against a database, you can also try to annotate them!

.. code-block:: yaml

   PARAMS:
      ASSEMBLY:
         OVERLAP_SIZE : 15
         FILTER_CONTIG_SIZE : 100


3.2. Adapt cluster_config.yaml
-------------------------------


If you will run ikiss in cluster, adapt `cluster_config.yaml` :  

.. code-block:: bash

   ikiss edit_cluster_config

Inside `cluster_config.yaml`, adapt partition to your favorite cluster and change memory and cpu number in by `__default__` key or in rules you need :

.. code-block:: bash

   __default__:
      cpus-per-task : 4
      mem-per-cpu : 10G
      partition : "normal"
      nodelist: node19
      output : 'slurm_logs/stdout/{rule}/{wildcards}.o'
      error : 'slurm_logs/error/{rule}/{wildcards}.e'
      job-name : '{rule}.{wildcards}'
      
   kmers_gwas_per_sample:
      cpus-per-task : 4
      mem-per-cpu : 10G


RULES  
-----

Here you can quickly find iKISS snakemake rules list : 

.. code-block:: bash

   rule kmers_gwas_per_sample *
   rule kmers_to_use
   rule kmers_table
   rule extract_kmers_from_bed
   rule index_ref
   rule mapping_kmers
   rule filter_bam *
   rule kmer_position_from_bam *
   rule merge_kmer_position
   rule pcadapt * 
   rule merge_pcadapt
   rule outliers_pcadapt_position
   rule get_pca_from_phenotype
   rule lfmm * 
   rule merge_lfmm
   rule outliers_lfmm_position
   rule mergetags_lfmm
   rule mergetags_pcadapt
   rule report_ikiss
   rule html_ikiss

* rules with a `*` can be parallelised.


4. Running iKISS
================

Run iKISS by `ikiss run_local` or `ikiss run_cluster` as explained in "Running a datatest" section.



5. iKISS output
================

This is a overwiew of iKISS output directory:

.. code-block:: bash

      OUTPUT-KISS/
      ├── 1.KMERS_MODULE
      │   ├── Clone1
      │   │   ├── Clone1_files.txt
      │   │   ├── Clone1_kmc3_all.kmc_pre
      │   │   ├── Clone1_kmc3_all.kmc_suf
      │   │   ├── Clone1_kmc3_canon.kmc_pre
      │   │   ├── Clone1_kmc3_canon.kmc_suf
      │   │   ├── Clone1_kmers_with_strand
      │   ├── Clone2
      │   └── CloneX
      ├── 2.KMERS_TABLE
      │   ├── kmers_table.names
      │   ├── kmers_table.table
      │   ├── kmers_to_use
      │   ├── kmers_to_use.no_pass_kmers
      │   ├── kmers_to_use.shareness
      │   ├── kmers_to_use.stats.both
      │   ├── kmers_to_use.stats.only_canonical
      │   ├── kmers_to_use.stats.only_non_canonical
      ├── 3.TABLE2BED
      │   ├── output_file.0.bed
      │   ├── output_file.0.bim
      │   └── output_file.0.fam
      ├── 4.EXTRACT_FASTQ
      │   └── output_file.0.fastq.gz
      ├── 5.RANGES
      │   └── output_file.0
      │       ├── 1.txt
      │       ├── 2.txt
      │       ├── 3.txt
      │       ├── 4.txt
      │       └── 5.txt
      ├── 6.LFMM
      │   ├── output_file.0_1_lfmm_outliers.csv
      │   ├── output_file.0_1_lfmm.rplot.pdf
      │   ├── output_file.0_2_lfmm_outliers.csv
      │   ├── output_file.0_2_lfmm.rplot.pdf
      │   ├── output_file.0_3_lfmm_outliers.csv
      │   ├── output_file.0_3_lfmm.rplot.pdf
      │   ├── output_file.0_4_lfmm_outliers.csv
      │   ├── output_file.0_4_lfmm.rplot.pdf
      │   ├── output_file.0_5_lfmm_outliers.csv
      │   └── output_file.0_5_lfmm.rplot.pdf
      ├── 6.PCADAPT
      │   ├── output_file.0_1_BH0.05.pcadapt_outliers.csv
      │   ├── output_file.0_1_BH0.05.pcadapt_pvalues.csv
      │   ├── output_file.0_1_BH0.05.pcadapt.rplot.pdf
      │   ├── output_file.0_1_BH0.05.pcadapt_scores.csv 
      │   ├ ...   
      ├── 7.MERGED_LFMM
      │   └── merged_lfmm_pvalues.csv
      ├── 7.MERGED_PCADAPT
      │   ├── merged_pcadapt_outliers.csv
      │   └── merged_pcadapt_pvalues.csv
      ├── 8.MAPPING
      │   ├── output_file.0_vs_reference.bam
      │   ├── output_file.0_vs_reference_F4MQ10.bam
      │   ├── output_file.0_vs_reference_sorted.bam
      │   ├── output_file.0_vs_reference_sorted.bam.stats
      │   └── REF
      ├── 9.KMERPOSITION
      │   └── output_file.0_vs_reference_KMERPOSITION.txt
      ├── 10.MERGE_KMERPOSITION
      │   ├── kmer_position_merged.txt
      ├── 11.OUTLIERS_LFMM_POSITION
      │   └── outliers_with_position.csv
      ├── 11.OUTLIERS_PCADAPT_POSITION
      │   └── outliers_with_position.csv
      ├── 12.ASSEMBLY_OUTLIER_PCADAPT
      │   └── outliers_pcadapt_mergetags.fasta
      ├── 12.ASSEMBLY_OUTLIER_LFMM
      │   └── outliers_lfmm_mergetags.fasta
      ├── BENCHMARK
      ├── LOGS
      └── config_corrected.yaml

Note : we recommended to remove 1.KMER_GWAS repertory after analysis.


Authors
========

Julie Orjuela (IRD)

Yves Vigouroux (IRD)


License
=======

Licensed under MIT.

Intellectual property belongs to IRD and authors.

iKISS uses recycled code from the culebrONT project of SouthGreen platform https://culebront-pipeline.readthedocs.io/en/latest/.
iKISS uses SnakEcdysis package https://snakecdysis.readthedocs.io/en/latest/package.html to perform installation and execution in local and cluster mode.

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.7%2B-blue
   :target: https://www.python.org/downloads
.. |SnakemakeVersions| image:: https://img.shields.io/badge/snakemake-≥5.10.0-brightgreen.svg?style=flat
   :target: https://snakemake.readthedocs.io
.. |Singularity| image:: https://img.shields.io/badge/singularity-≥3.3.0-7E4C74.svg
   :target: https://sylabs.io/docs/
.. |readthedocs| image:: https://pbs.twimg.com/media/E5oBxcRXoAEBSp1.png
   :target: https://culebront-pipeline.readthedocs.io/en/latest/
   :width: 400px


