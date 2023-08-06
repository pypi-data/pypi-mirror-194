#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from ikiss.global_variables import GIT_URL, DOCS, DATATEST_URL_FILES, SINGULARITY_URL_FILES
from ikiss.module import IKISS

logo = Path(__file__).parent.resolve().joinpath('logo_ikiss.png').as_posix()
__version__ = Path(__file__).parent.resolve().joinpath("VERSION").open("r").readline().strip()
__doc__ = """ iKISS is a pipeline to identify kmers under selection  """

description_tools = f"""
    Welcome to iKISS version: {__version__} ! 
    @author: Julie Orjuela (IRD)
    @email: julie.orjuela@ird.fr
    Please cite our git: {GIT_URL}
    Licenced under MIT 
    Intellectual property belongs to IRD and authors."""

dico_tool = {
    "soft_path": Path(__file__).resolve().parent.as_posix(),
    "url": GIT_URL,
    "docs": DOCS,
    "description_tool": description_tools,
    "singularity_url_files": SINGULARITY_URL_FILES,
    "datatest_url_files": DATATEST_URL_FILES,
    "snakefile": Path(__file__).resolve().parent.joinpath("Snakefile"),
    "snakemake_scripts": Path(__file__).resolve().parent.joinpath("snakemake_scripts")
}