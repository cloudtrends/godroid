# -*- coding: utf-8 –*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs


import sub_gene_class, sub_gene_funcs_gorp, sub_gene_api, sub_gene_comm

def log(line):
    comm_funcs.print_ok("   godroid_helper  :" + line )
def error(line):
    comm_funcs.print_error("   godroid_helper  :" + line )


def print_profile_instance_obj( obj ):
    print "--- --- --- --- --- --- --- --- BEGIN"
    print "table_name:", obj.TableName
    print "class_name:", obj.ClassName
    print "columns:"
    print "\t\t--- --- --- --- B"
    for one in obj.ColumnsList:
        print "\t\t", one.SqlName, one.SqlType, one.GoName, one.GoType
    print "\t\t--- --- --- --- E"
    print "--- --- --- --- --- --- --- --- END"

def get_instance_profile_from_profile_file( profile_path ):
    log("begin get instance from profile:" + profile_path)
    tmp_cls = sub_gene_comm.ClassProfileCfg()
    tmp_cls.ProfileFile = profile_path
    contents_list = comm_funcs.get_file_content_as_list(profile_path)
    for line in contents_list:
        line = line.strip()
        if 0 == len(line):
            continue
        if line.startswith("#"):
            continue
        if line.startswith("table_name=") :
            line = line.replace("table_name=", "")
            tmp_cls.TableName = line.strip()
        if line.startswith("package_name="):
            line = line.replace("package_name=", "")
            tmp_cls.PackageName = line.strip()
        if line.startswith("class_name=") :
            line = line.replace("class_name=", "")
            tmp_cls.ClassName = line.strip()
        if line.startswith( "columns=" ) :
            line = line.replace("columns=", "").strip()
            obj = sub_gene_comm.ClassColumnProfile()
            lines = line.split(";")
            sql_part = lines[0]
            go_part = lines[1]
            sql_parts = sql_part.split(",")
            go_parts = go_part.split(",")
            obj.SqlName = sql_parts[0]
            obj.SqlType = sql_parts[1]
            obj.GoName = go_parts[0]
            obj.GoType = go_parts[1]
            tmp_cls.ColumnsList.append(obj)
    return tmp_cls







### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


def get_domain_model_path(model_domain):
    gopath = comm_funcs.get_gopath()
    return gopath + "/src/" + model_domain + "/model"
def get_domain_api_path(model_domain):
    gopath = comm_funcs.get_gopath()
    return gopath + "/src/" + model_domain + "/api"

def get_domain_model_instance_full_path(profile_instance, model_domain):
    return get_domain_model_path(model_domain) + "/" + profile_instance.PackageName 
    pass
def get_domain_api_instance_full_path(profile_instance, model_domain):
    return get_domain_api_path(model_domain) + "/" + profile_instance.PackageName  
    pass

#---------------

def get_model_class_file_name(profile_instance):
    model_file_name = "m_" + profile_instance.PackageName + profile_instance.FileExt
    return model_file_name
def get_model_funcs_of_gorp_file_name(profile_instance):
    funcs_of_gorp_file_name = "funcs_of_gorp"  + profile_instance.FileExt
    return funcs_of_gorp_file_name
def get_api_file_name(profile_instance):
    api_file_name = "api_" + profile_instance.PackageName + profile_instance.FileExt
    return api_file_name

def get_model_funcs_of_gorp_file_name_full_path(profile_instance, model_domain):
    return get_domain_model_instance_full_path(profile_instance, model_domain) + "/" + get_model_funcs_of_gorp_file_name(profile_instance)
def get_model_class_file_name_full_path(profile_instance, model_domain):
    return get_domain_model_instance_full_path(profile_instance, model_domain) + "/" + get_model_class_file_name(profile_instance)
def get_api_file_name_full_path(profile_instance, model_domain):
    return get_domain_api_instance_full_path(profile_instance, model_domain)+ "/" + get_api_file_name(profile_instance)

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


def touch_and_create_empty_file(file_full_path, profile_instance):
    """
    by default , should check 3 files : model , funcs of gorp and api
    the name of each file should not changed

    check include:
        1. magic header
                package xxxx
                //magic  version: xxxx   generatedby: xxxx
        2. //meta flag begin
           //meta flag end
    """
    #touch
    #create empty file with meta flags
    comm_funcs.touch(file_full_path)
    template_lines = sub_gene_comm.GoEmptyFileTemplate
    template_lines = template_lines.replace( "PACKAGENAME", profile_instance.PackageName )
    comm_funcs.add_to_exist_file(file_full_path, template_lines)


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def check_model_funcs_api_meta_flag( profile_instance, model_domain ):
    #gopath = comm_funcs.get_gopath()
    #model_file_name = get_model_class_file_name( profile_instance )
    #funcs_of_gorp_file_name = get_model_funcs_of_gorp_file_name( profile_instance )
    #api_file_name = get_api_file_name( profile_instance )
    #
    domain_model_instance_full_path = get_domain_model_instance_full_path(profile_instance, model_domain)
    if not os.path.exists( domain_model_instance_full_path ):
        comm_funcs.print_ok("TIPS:")
        comm_funcs.print_ok("......create for :" + domain_model_instance_full_path )
        os.makedirs(domain_model_instance_full_path)
    domain_api_instance_full_path = get_domain_api_instance_full_path(profile_instance, model_domain)
    if not os.path.exists( domain_api_instance_full_path ):
        comm_funcs.print_ok("TIPS:")
        comm_funcs.print_ok("......create for :" + domain_api_instance_full_path )
        os.makedirs(domain_api_instance_full_path)


    FullPathModelFile = get_model_class_file_name_full_path(profile_instance, model_domain)
    FullPathFuncsOfGropFile = get_model_funcs_of_gorp_file_name_full_path(profile_instance, model_domain)
    FullPathApiFile = get_api_file_name_full_path(profile_instance, model_domain)
    if not os.path.exists(FullPathModelFile):
        touch_and_create_empty_file(FullPathModelFile, profile_instance)
    if not os.path.exists(FullPathFuncsOfGropFile) :
        touch_and_create_empty_file(FullPathFuncsOfGropFile, profile_instance)
    if not os.path.exists(FullPathApiFile):
        touch_and_create_empty_file(FullPathApiFile, profile_instance)
    if True:
        comm_funcs.print_ok(">>>> begin check meta flag is valid")
        model_class_valid = False
        funcs_of_gorp_valid = False
        api_file_valid = False
        #
        model_class_valid = sub_gene_class.__check_model_meta_flag(FullPathModelFile)
        funcs_of_gorp_valid = sub_gene_funcs_gorp.__check_funcs_meta_flag(FullPathFuncsOfGropFile)
        api_file_valid = sub_gene_api.__check_api_meta_flag(FullPathApiFile)
        if model_class_valid and funcs_of_gorp_valid and api_file_valid:
            return True
        else:
            comm_funcs.print_error("PYTHON ERROR: check files meta flag valid is false !  EXIT NOW ")
            sys.exit(1)
        pass
    #sub_gene_class, sub_gene_funcs_gorp, sub_gene_api
    return True


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def __check_instance_profile_columns( contents ):
    for line in contents:
        if not line.startswith("columns="):
            continue
        line = line.replace("columns=", "")
        lines = line.split(";")
        if 2 != len(lines):
            error(" cfg file columns not valid ( X,X;X,X ) :" + line )
            sys.exit(1)
        #columns=id,int;Id,int
        first_part = lines[0]
        second_part = lines[1]
        first_parts = first_part.split(",")
        second_parts = second_part.split(",")
        if not 2 == len(first_parts) and not 2 == len(second_parts):
            error(" cfg file columns not valid ( X,X;X,X ) :" + line )
            sys.exit(1)

    return True



def __check_instance_profile_class_name( contents ):
    for line in contents:
        if line.startswith("table_name="):
            pass
        if line.startswith("class_name"):
            line = line.replace("class_name=", "")
            one_char = line[:1]
            char_int = ord(one_char)
            if char_int >= 65 and char_int <= 90:
                pass
            else:
                error( " Class should Begin with UpperCase !!EXIT . " )
                sys.exit(1)
            log( "one_char:" + str(  char_int ) )
            pass
        if line.startswith("columns"):
            pass
    return True
    pass


def __check_instance_profile_items_exists( contents ):
    for line in contents:
        if line.startswith("table_name="):
            pass
        if line.startswith("class_name"):
            pass
        if line.startswith("columns"):
            pass
    return True
    pass


    



def check_instance_profile(  instance_profile_path = None ):
    """
    """
    log("begin check_instance_profile :" + instance_profile_path )
    contents_list = comm_funcs.get_file_content_as_list(instance_profile_path)
    if __check_instance_profile_items_exists(contents_list):
        pass
    if __check_instance_profile_class_name(contents_list):
        pass
    if __check_instance_profile_columns(contents_list):
        pass
    return True
