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

import sub_gene_class, sub_gene_funcs_gorp, sub_gene_api, sub_gene_comm, godroid_helper, sub_gene_controller, sub_gene_api_web_module, sub_gene_revel_curd, sub_gene_html_curd


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def print_ok(line):
    comm_funcs.print_ok("   GENERATOR  :" + line )
def print_error(line):
    comm_funcs.print_error("   GENERATOR  :" + line )


def help():
    print "--- --- --- --- --- --- --- HELP --- --- --- --- --- "
    print "argv1:", "profile_file.cfg"
    print "argv2:", "ModelDomain , such as  bar.com foo.com "
    comm_funcs.print_ok("argv3: Generate Content type, such as : module;controller;html ")



def check_and_get_go_path():
    return comm_funcs.check_and_get_go_path()


def __self_call_generate_api_web_module(instance_profile_obj, model_domain):
    """
    api_web_module
    """
    if not godroid_helper.check_api_web_module_meta_flag(instance_profile_obj , model_domain):
        print_error("ERROR: api_web_module meta flag check failed: " + instance_profile_obj.ProfileFile )
        sys.exit(1)
    sub_gene_api_web_module.generate_apiwebmodule_file(instance_profile_obj, model_domain)


def __self_call_generate_revel_curd_funcs(instance_profile_obj, model_domain):
    """
    revel_curd_funcs
    revelcurdfuncs
    """
    if not godroid_helper.check_revel_curd_funcs_meta_flag(instance_profile_obj , model_domain):
        print_error("ERROR: api_web_module meta flag check failed: " + instance_profile_obj.ProfileFile )
        sys.exit(1)
    sub_gene_revel_curd.generate_revelcurdfuncs_file(instance_profile_obj, model_domain)


def __self_call_generate_html(instance_profile_obj, model_domain):
    """
    generate html code for frantend and backend

    do not need check meta flag , because runing just once! only


    frantend html code list:
        index
        list

    backend html code list: (rableapp css style )
        index
        list
        add
        new
        save_new
        edit
        save_edit
        save_new
        get_one
    """
    print_ok("generate html func not DO NOT NEED CHECK META FLAG , JUST DELETE OLD FINE IS OK")
    print_ok(" generate html ONLY support DEV mode ")
    if instance_profile_obj.IsDevMode:
        sub_gene_html_curd.generate_htmlcurl_file(instance_profile_obj, model_domain)
        pass


    pass


def __self_call_generate_controller(instance_profile_obj, model_domain):
    """
    sub_gene_controller.py
    """
    if not godroid_helper.check_controller_meta_flag(instance_profile_obj , model_domain):
        comm_funcs.print_error("ERROR: controller meta flag check failed: " + instance_profile_obj.ProfileFile )
        sys.exit(1)

    if len(instance_profile_obj.ControlCalssName) == 0:
        comm_funcs.print_error("Tips:")
        comm_funcs.print_ok("ControlCalssName not exist so return .")
        sys.exit(1)
    comm_funcs.print_ok("X : generate the controller and controller_admin file ")
    #if not godroid_helper.check_controller_meta_flag(instance_profile_obj, model_domain):
    #    comm_funcs.print_error("ERROR: controller meta flag check failed:" + instance_profile_obj.ProfileFile)
    #    sys.exit(1)
    #    pass
    sub_gene_controller.generate_controller_file(instance_profile_obj, model_domain)
    pass

def __self_call_generate_model_class_gorp_funcs_and_api(instance_profile_obj, model_domain):
    """
    if file exist , check have meta tag
                        if have meta , then replace them
                        if not have meta tag , just give hint and stop
    if not exists , create new 
    """
    #sub_gene_class, sub_gene_funcs_gorp, sub_gene_api
    if not godroid_helper.check_model_funcs_api_meta_flag( instance_profile_obj , model_domain):
        comm_funcs.print_error("ERROR: model funcs api meta flag check failed :" + instance_profile_obj.ProfileFile )
        sys.exit(1)

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
    if 5 != len(sys.argv):
        help()
        comm_funcs.print_error("PYTHON ERROR: shoud assign: prod/dev mode, class profile file , model domain , module;controller;html;")
        sys.exit(1)
    gopath = comm_funcs.check_and_get_go_path()
    sub_gene_comm.check_model_profile_exist()
    run_mode = sys.argv[1]
    profile_file = sys.argv[2]
    model_domain = sys.argv[3]
    generate_components = sys.argv[4]
    sub_gene_comm.check_and_create_model_domain_path(model_domain, gopath)
    InstanceProfilePath = sub_gene_comm.get_full_profile_instance_path(profile_file)
    # model_profile/models
    # check is generated
    instance_profile_obj = godroid_helper.get_instance_profile_from_profile_file( InstanceProfilePath )
    if len(instance_profile_obj.ControlCalssName) == 0:
        comm_funcs.print_error("Tips:")
        comm_funcs.print_ok("ControlCalssName not exist so return .")
        sys.exit(1)

    #
    if "dev" == run_mode:
        instance_profile_obj.IsDevMode = True
        pass
    elif "prod" == run_mode:
        instance_profile_obj.IsDevMode = False
        pass
    #

    if "module" in generate_components or "all" in generate_components:
        comm_funcs.print_ok("... ... begin convert model cfg file to instance profile")
        godroid_helper.print_profile_instance_obj(instance_profile_obj)  # this is a helper class, for print the content of cfg
        comm_funcs.print_ok("... ... instance_profile_obj ok ,continue " )
    #
    #
    if "module" in generate_components  or "all" in generate_components:
        __self_call_generate_model_class_gorp_funcs_and_api( instance_profile_obj , model_domain )
    if "controller" in generate_components  or "all" in generate_components:
        # execute this function at last
        __self_call_generate_controller(instance_profile_obj , model_domain)
    if "html" in generate_components  or "all" in generate_components:
        #auto generate  routes
        #auto generate  html pieces , frantend and backend
        # html code should just generate once, or , if exist already , do nothing
        __self_call_generate_html(instance_profile_obj , model_domain)
    if "all" in generate_components:
        comm_funcs.print_ok("begin generate : api/web/<module_name>  funcs for web layercall")
        comm_funcs.print_ok("\t\t\t\t\t\tif module_name is empty , use gobbs as default")
        __self_call_generate_api_web_module(instance_profile_obj , model_domain)
    if "all" in generate_components:
        comm_funcs.print_ok("begin generate : revel template funcs for CURD ")
        __self_call_generate_revel_curd_funcs(instance_profile_obj, model_domain)

    

    
