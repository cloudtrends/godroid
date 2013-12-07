# -*- coding: utf-8 –*-
"""Usage:
  quick_example.py tcp <host> <port> [--timeout=<seconds>]
  quick_example.py serial <port> [--baud=9600] [--timeout=<seconds>]
  quick_example.py -h | --help | --version



"""
#https://github.com/docopt/docopt/tree/master/examples
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs

import sub_gene_class, sub_gene_funcs_gorp, sub_gene_api, sub_gene_comm, godroid_helper
from docopt import docopt



if "__main__" == __name__:
    arguments = docopt(__doc__, version='0.1.1rc')
    print_ok(arguments)
    comm_funcs.print_ok("begin generate cfg ... ")
    """
    generate the cfg files
    """
    tmplt_name = "zhaopin_person_basic.tmplt"
    bb = "cfg_templates"

    json_content = comm_funcs.get_file_content_as_list( tmplt_name )
    gopath = comm_funcs.check_and_get_go_path()
    #ClassCfgTemplate
    #ClassColumnCfgTemplateProfile
    sub_gene_comm.check_model_profile_exist()
    

"""
"""

