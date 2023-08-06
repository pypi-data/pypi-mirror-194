#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .global_variables import *
from snakecdysis import *

class IKISS(SnakEcdysis):
    """
    class IKISS creates an object with fastq attributes and self functions (adapted from CulebrONT)
    """

    def __init__(self, dico_tool, workflow, config):
        super().__init__(**dico_tool, workflow=workflow, config=config)
        self.config = config
        self.fastq_files_list = []
        self.fastq_files_ext = []
        self.fastq_names_list = []
        self.fastq_gzip = None
        self.ref = None
        self.samples = {}
        self.phenotype = {}
        self.mapping_mode = 'bwa-aln'

        self.forward = ""
        self.reverse = ""

        self.use_env_modules = workflow.use_env_modules
        self.use_conda = workflow.use_conda
        self.use_singularity = workflow.use_singularity

        self.__check_config_dic()
        self.__split_illumina()

        # checked config.yaml:
        self.write_config(f"{self.config['DATA']['OUTPUT']}/config_corrected.yaml")

    def __split_illumina(self):
        forward = []
        reverse = []
        for fastq in self.fastq_files_list:
            if '_R1' in fastq:
                forward.append(fastq)
            elif '_1' in fastq:
                forward.append(fastq)
            elif '_R2' in fastq:
                reverse.append(fastq)
            elif '_2' in fastq:
                reverse.append(fastq)
        return forward, reverse

    def __check_config_dic(self):
        """Configuration file checking"""

        self.tools_activated = self.__build_tools_activated("WORKFLOW", ("KMERS_MODULE", "PCADAPT", "LFMM", "MAPPING", "ASSEMBLY"), True)

        # check mandatory directory
        self._check_dir_or_string(level1="DATA", level2="OUTPUT")
        self._check_dir_or_string(level1="DATA", level2="FASTQ")

        def get_mapping_mode(self, list):
            if self in list:
                #print (self)
                return self
            else:
                raise ValueError(
                    f"CONFIG FILE CHECKING FAIL : you need to chose between {ALLOW_MAPPING_MODE} in MAPPING mode !")

        def get_dico_samples_and_pop(self, path):
            # check of header
            infile = open(path, 'r')
            if not 'accession_id\tphenotype_value' in infile.readline():
                raise ValueError(
                    f"SAMPLES FILE CHECKING FAIL : Please add accession_id\tphenotype_value in SAMPLES tabulated header !")
            infile.close()
            # populating self.samples
            with open(path, "r") as samples_open:
                for line in samples_open:
                    if not 'accession_id' in line:
                        key, value = line.strip().split('\t')
                        self.samples[key] = value
            #print ("SAMPLES")
            #print(self.samples)
            return self.samples


        def get_dico_phenotype_and_pop(self, path):
            # check of header
            infile = open(path, 'r')
            if not 'accession_id\tgroup' in infile.readline():
                raise ValueError(
                    f"PHENOTYPE_FILE CHECKING FAIL : Please add accession_id\tgroup in PHENOTYPE_FILE tabulated header !")
            infile.close()
            # populating self.samples
            with open(path, "r") as phenotype_open:
                for line in phenotype_open:
                    if not 'accession_id' in line:
                        key, *value = line.strip().split('\t')
                        self.phenotype[key] = value
            #print("PHENO")
            #print(self.phenotype)
            return self.phenotype


        # pick fastq and extension
        self.fastq_files_list, fastq_files_list_ext = get_files_ext(self.get_config_value(level1='DATA', level2='FASTQ'), ALLOW_FASTQ_EXT)
        if not self.fastq_files_list:
            raise ValueError(
                f"CONFIG FILE CHECKING FAIL : you need to append at least on fastq with extension on {ALLOW_FASTQ_EXT}")
        # check if all fastq have the same extension
        if len(fastq_files_list_ext) > 1:
            raise ValueError(
                f"CONFIG FILE CHECKING FAIL : Please use only the same format for assembly FASTQ data, not: {fastq_files_list_ext}")
        else:
            self.fastq_files_ext = fastq_files_list_ext[0]
        # check if fastq are gzip
        if "gz" in self.fastq_files_ext:
            self.fastq_gzip = True

        self.forward, self.reverse = self.__split_illumina()

        self.mapping_mode = get_mapping_mode(self.config['PARAMS']['MAPPING']['MODE'], ALLOW_MAPPING_MODE)

        # get dico with samples names as key and population as value.
        self.samples = get_dico_samples_and_pop(self, self.get_config_value(level1='PARAMS', level2='PCADAPT', level3='SAMPLES'))
        self.phenotype = get_dico_phenotype_and_pop(self, self.get_config_value(level1='PARAMS', level2='LFMM', level3='PHENOTYPE_FILE'))

        # get samples name from reads files
        for elem in self.fastq_files_list:
            if '_R1' in elem :
                fastq_name = Path(elem).stem.split('_R1')[0]
                self.fastq_names_list.append(fastq_name)
            if '_1' in elem or '_1' in elem:
                fastq_name = Path(elem).stem.split('_1')[0]
                self.fastq_names_list.append(fastq_name)


        # comparing names from reads and names from samples.txt given by user
        if sorted(self.fastq_names_list) != sorted(list(self.samples.keys())) :
            #print(sorted(self.fastq_names_list))
            #print(sorted(list(self.samples.keys())))
            print ("samples in FASTQ but not in SAMPLES")
            print(set(sorted(self.fastq_names_list)) - set(sorted(list(self.samples.keys()))))
            print ("samples in SAMPLES but not in FASTQ")
            print(set(sorted(list(self.samples.keys()))) - set(sorted(self.fastq_names_list)))
            raise ValueError(f"CONFIG FILE CHECKING ERROR : FASTQ names and SAMPLES names are different. Please check your samples file !")
            # @seb ? raise ValueError(f"Invalid argument `key_value_pairs`! SAMPLES file is corrupted, use only tabulations, don't put a header in SAMPLES file")

        # comparing names from reads and names from phenotype.txt given by user
        if sorted(self.fastq_names_list) != sorted(list(self.phenotype.keys())) :
            #print(sorted(self.fastq_names_list))
            #print(sorted(list(self.phenotype.keys())))
            print ("samples in FASTQ but not in PHENOTYPE")
            print(set(sorted(self.fastq_names_list)) - set(sorted(list(self.phenotype.keys()))))
            print ("samples in SAMPLES but not in PHENOTYPE")
            print(set(sorted(list(self.phenotype.keys()))) - set(sorted(self.fastq_names_list)))
            raise ValueError(f"CONFIG FILE CHECKING ERROR : FASTQ names and PHENOTYPE names are different. Please check your phenotype file !")
            # @seb ? raise ValueError(f"Invalid argument `key_value_pairs`! SAMPLES file is corrupted, use only tabulations, don't put a header in SAMPLES file")


        # kmers_module is obligatory and has to be activated,
        if not bool(self.config['WORKFLOW']['KMERS_MODULE']):
            raise ValueError(
                f"CONFIG FILE CHECKING ERROR : KMERS_MODULE is the minimal step you need to activate in the configuration file !! \n")

        # if mapping is true pcadapt or lfmm has to be activated
        if not self.config['WORKFLOW']['PCADAPT'] and not self.config['WORKFLOW']['LFMM'] and self.config['WORKFLOW']['MAPPING']:
            raise ValueError(
                f"CONFIG FILE CHECKING ERROR : MAPPING is irrelevant if you have not activated PCADAPT or LFMM !! \n")


        # check if reference is given by user if mapping is activate
        if self.config['WORKFLOW']['MAPPING']:
            self._check_file_or_string(level1="PARAMS", level2="MAPPING", level3="REF", mandatory=['MAPPING'])

        # check if phenotype file is correct if LFMM is activated
        if self.config['WORKFLOW']['LFMM']:
            self._check_file_or_string(level1="PARAMS", level2='LFMM', level3="PHENOTYPE_FILE", mandatory=['LFMM'])
            if not int(self.config['PARAMS']['PCADAPT']['K']):
                # TODO: je n'arrive pas a recuperer le bon error du raise
                raise TypeError(
                    f"CONFIG FILE CHECKING ERROR :  PARAMS/LFMM/K is not a integer !! \n")

        # check if samples file is correct if PCADAPT is activated
        if self.config['WORKFLOW']['PCADAPT']:
            self._check_file_or_string(level1="PARAMS", level2="PCADAPT", level3="SAMPLES", mandatory=['PCADAPT'])
            if type(self.config['PARAMS']['PCADAPT']['K']) is not int:
                raise f"CONFIG FILE CHECKING ERROR :  PARAMS/PCADAPT/K is not a integer !! \n"


    def __check_tools_config(self, tool, mandatory=[]):
        """Check if path is a file if not empty
        :return absolute path file"""
        tool_OK = True

        # If only envmodule
        if self.use_env_modules and not self.use_singularity:
            envmodule_key = self.tools_config["ENVMODULE"][tool]
            if not envmodule_key:
                raise ValueError(
                    f'CONFIG FILE CHECKING FAIL : please check tools_config.yaml in the "ENVMODULE" section, {tool} is empty')
            tool_OK = True

        # If envmodule and singularity
        if self.use_env_modules and self.use_singularity:
            raise ValueError(
                f"CONFIG FILE CHECKING FAIL : Use env-module or singularity but don't mix them")

        if len(mandatory) > 0 and not tool_OK:
            raise FileNotFoundError(
                f'CONFIG FILE CHECKING FAIL : please check tools_config.yaml in the  {tool} params, please append Singularity or module load, is mandatory for tool: {" ".join(mandatory)}')


    def __build_tools_activated(self, key, allow, mandatory=False):
        tools_activate = []
        for tool, activated in self.config[key].items():
            if tool in allow:
                boolean_activated = var_2_bool(key, tool, activated)
                if boolean_activated:
                    tools_activate.append(tool)
                    self.config[key][tool] = boolean_activated
                    self.__check_tools_config(tool, [tool])
            else:
                raise ValueError(f'CONFIG FILE CHECKING FAIL : {key} {tool} not allow on iKISS"')
        if len(tools_activate) == 0 and mandatory:
            raise ValueError(f"CONFIG FILE CHECKING FAIL : you need to set True for at least one {key} from {allow}")
        return tools_activate


    def __var_2_bool(self, key, tool, to_convert):
        """convert to boolean"""
        if isinstance(type(to_convert), bool):
            return to_convert
        elif f"{to_convert}".lower() in ("yes", "true", "t"):
            return True
        elif f"{to_convert}".lower() in ("no", "false", "f"):
            return False
        else:
            raise TypeError(
                f'CONFIG FILE CHECKING FAIL : in the "{key}" section, "{tool}" key: "{to_convert}" is not a valid boolean')


