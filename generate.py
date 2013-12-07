# -*- coding: utf-8 –*-
"""Usage:
  generate.py tcp <host> <port> [--timeout=<seconds>]
  generate.py serial <port> [--baud=9600] [--timeout=<seconds>]
  generate.py -h | --help | --version



"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs

import sub_gene_class, sub_gene_funcs_gorp, sub_gene_api, sub_gene_comm, godroid_helper

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


def help():
    print "--- --- --- --- --- --- --- HELP --- --- --- --- --- "
    print "argv1:", "profile_file.cfg"
    print "argv2:", "ModelDomain , such as  bar.com foo.com "



def check_and_get_go_path():
    return comm_funcs.check_and_get_go_path()



def __self_call_generate_model_class_gorp_funcs_and_api(instance_profile_obj, model_domain):
    """
    if file exist , check have meta tag
                        if have meta , then replace them
                        if not have meta tag , just give hint and stop
    if not exists , create new 
    """
    comm_funcs.print_ok("\n\n")
    comm_funcs.print_ok("--- --- --- --- --- --- now begin generate code ... ... ... ... ... ")
    sub_gene_class.generate_model_class_file(instance_profile_obj, model_domain)
    sub_gene_funcs_gorp.generate_funcs_of_gorp_file(instance_profile_obj, model_domain)
    sub_gene_api.generate_api_file(instance_profile_obj, model_domain)
    comm_funcs.print_ok("--- --- --- --- --- --- now begin generate code ... ... ... ... ... end")
    comm_funcs.print_ok("\n\n")
    pass


if __name__ == "__main__":
    """

    """
    if 3 != len(sys.argv):
        help()
        comm_funcs.print_error("PYTHON ERROR: shoud assign class profile file , model domain ")
        sys.exit(1)
    gopath = comm_funcs.check_and_get_go_path()
    sub_gene_comm.check_model_profile_exist()
    profile_file = sys.argv[1]
    model_domain = sys.argv[2]
    sub_gene_comm.check_and_create_model_domain_path(model_domain, gopath)
    InstanceProfilePath = sub_gene_comm.get_full_profile_instance_path(profile_file)
    # model_profile/models
    # check is generated
    comm_funcs.print_ok("... ... begin convert model cfg file to instance profile")
    instance_profile_obj = godroid_helper.get_instance_profile_from_profile_file( InstanceProfilePath )
    godroid_helper.print_profile_instance_obj(instance_profile_obj)  # this is a helper class, for print the content of cfg
    comm_funcs.print_ok("... ... instance_profile_obj ok ,continue " )
    #
    #sub_gene_class, sub_gene_funcs_gorp, sub_gene_api
    if not godroid_helper.check_model_funcs_api_meta_flag( instance_profile_obj , model_domain):
        comm_funcs.print_error("ERROR: model funcs api meta flag check failed :" + instance_profile.ProfileFile )
        sys.exit(1)
    __self_call_generate_model_class_gorp_funcs_and_api( instance_profile_obj , model_domain )
    

    
