import nbformat as nbf
import argparse
from pathlib import Path, PurePosixPath

nb = nbf.v4.new_notebook()
nb['cells'] = []

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-p", "--phenotype_file", help="phenotype file with variables continuos", type=str)
parser.add_argument("-o", "--output_file", help="output file", type=str)

args = parser.parse_args()
pheno = args.phenotype_file
pheno = Path(pheno).resolve()
name_pheno = PurePosixPath(pheno).stem
dir_pheno = PurePosixPath(pheno).parent

jupyter = args.output_file
jupyter = f"{Path(jupyter).resolve()}"
name_jupyter = PurePosixPath(jupyter).stem
dir_jupyter = PurePosixPath(jupyter).parent
csv = f"{dir_jupyter}/{name_jupyter}.csv"

texte = f"""\
# KISS REPORT

### 
This is an auto-generated jupyter notebook from iKISS package to calculate stats obtained in different steps of pipeline.
"""
code = f"""\
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA"""

nb['cells'].append(nbf.v4.new_markdown_cell(texte))
nb['cells'].append(nbf.v4.new_code_cell(code))





