# -*- coding: utf-8 –*-
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
    gopath = comm_funcs.get_gopath()
    if gopath is None or 0 == len(gopath):
        comm_funcs.print_error("ERROR: evn go path not set ")
        sys.exit(1)
    return gopath 

if __name__ == "__main__":
    """

    """
    if 3 != len(sys.argv):
        help()
        comm_funcs.print_error("PYTHON ERROR: shoud assign class profile file , model domain ")
        sys.exit(1)
    ModelProfileDirName = "model_profile"
    AlreadyGeneratedModelProfileName = "already_generated_model_profile.txt"
    gopath = check_and_get_go_path()
    ModelProfilePath = gopath + "/" + ModelProfileDirName
    ModelProfileModelsPath = gopath + "/" + ModelProfileDirName + "/models"
    if not os.path.exists( ModelProfilePath + "/" +  AlreadyGeneratedModelProfileName ):
        comm_funcs.print_error("ERROR: already profile config not exist. ")
        sys.exit(1)
    profile_file = sys.argv[1]
    model_domain = sys.argv[2]
    ModelDomainFullPath = gopath + "/src/" + model_domain
    sub_gene_comm.check_and_create_model_domain_path(ModelDomainFullPath, gopath)
    if not profile_file.endswith(".cfg"):
        comm_funcs.print_error("ERROR: profile file extension not match cfg:" + profile_file)
        sys.exit(1)
    InstanceProfilePath = ModelProfileModelsPath + "/" + profile_file
    if not os.path.exists(InstanceProfilePath):
        comm_funcs.print_error("ERROR: profile file not exist:" + InstanceProfilePath)
        sys.exit(1)
    # model_profile/models
    # check is generated
    # 
    comm_funcs.print_ok("begin check profile file :" + InstanceProfilePath)
    if not godroid_helper.check_instance_profile(InstanceProfilePath):
        comm_funcs.print_error("ERROR: profile file check failed :" + InstanceProfilePath)
        sys.exit(1)
    #instance_profile = sub_gene_comm.ClassProfileCfg()
    comm_funcs.print_ok("... ... begin convert model cfg file to instance profile")
    instance_profile = godroid_helper.get_instance_profile_from_profile_file( InstanceProfilePath )
    #
    if instance_profile is None:
        comm_funcs.print_error("PYTHON ERROR: instance profile is Error. ")
        sys.exit(1)
    godroid_helper.print_profile_instance_obj(instance_profile)  # this is a helper class, for print the content of cfg
    comm_funcs.print_ok("instance_profile ok ,continue " )
    """
    if file exist , check have meta tag
                        if have meta , then replace them
                        if not have meta tag , just give hint and stop
    if not exists , create new 
    """
    if not godroid_helper.check_model_funcs_api_meta_flag( instance_profile , model_domain):
        comm_funcs.print_error("ERROR: model funcs api meta flag check failed :" + instance_profile.ProfileFile )
        sys.exit(1)
    #
    comm_funcs.print_ok("\n\n")
    comm_funcs.print_ok("--- --- --- --- --- --- now begin generate code ... ... ... ... ... ")
    #sub_gene_class, sub_gene_funcs_gorp, sub_gene_api
    sub_gene_class.generate_model_class_file(instance_profile, model_domain)
    sub_gene_funcs_gorp.generate_funcs_of_gorp_file(instance_profile, model_domain)
    sub_gene_api.generate_api_file(instance_profile, model_domain)
    comm_funcs.print_ok("--- --- --- --- --- --- now begin generate code ... ... ... ... ... end")
    comm_funcs.print_ok("\n\n")
    

    
