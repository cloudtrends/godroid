# -*- coding: utf-8 –*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import time
import comm_funcs

GoTemplateMagicSecondLine = "//magic_meta_v1_header_flag"

GoTemplateAutoPartBegin = "//magic_meta_v1_auto_part_begin"
GoTemplateAutoPartEnd = "//magic_meta_v1_auto_part_end"

GoTemplateCustomPartBegin = "//magic_meta_v1_custom_part_begin"
GoTemplateCustomPartEnd = "//magic_meta_v1_custom_part_end"

# model profile config
#=====================
ModelProfileDirName = "model_profile"
AlreadyGeneratedModelProfileName = "already_generated_model_profile.txt"


GoEmptyFileTemplate="""package PACKAGENAME

//magic_meta_v1_header_flag  version: v131117   generatedby: v131117

//magic_meta_v1_auto_part_begin
//magic_meta_v1_auto_part_end

//magic_meta_v1_custom_part_begin
//magic_meta_v1_custom_part_end

    """



class ClassColumnCfgTemplateProfile:
    SqlName = ""
    Type = ""
    Length = ""
    ShowName = ""

class ClassCfgTemplate:
    PackageName = ""
    TableName = ""
    ClassName = ""
    FuncName = ""


class ClassFileContent():
    def __init__(self):
        pass
    BeforeMetaFlagContent = ""
    MetaFlagContent = ""
    AfterMetaFlagContent = ""


class ClassColumnProfile:
    def __init__(self):
        pass
    #columns=my_id,varchar(30);MyId,string
    SqlName = ""
    SqlType = ""
    GoName = ""
    GoType = ""
    ShowName = ""

class ClassProfileCfg:
    def __init__(self):
        pass
    IsDevMode = True 
    IsModule = False
    GeneCompontents = ""
    ModuleType = ""
    ModuleName = ""
    ControlCalssName = ""
    
    PackageName = ""
    FuncName = ""
    TableName = ""
    ClassName = ""
    ColumnsList = []
    ProfileFile = ""
    FileExt = ".go"


class ClassModelGorpApiGoFile:
    def __init__(self):
        pass



def get_all_sql_fileds_params_str(profile_instance):
    '''
    this function used for : golang code , auto set fields as golang parameters.
                by append with : string  or  int  variables type
    :param profile_instance:
    :return:
    '''
    int_str = ""
    str_str = ""
    for one in profile_instance.ColumnsList:
        if one.SqlType.startswith("int"):
            int_str = int_str + one.SqlName + ", "
            pass
        if one.SqlType.startswith("char"):
            str_str = str_str + one.SqlName + ", " 
            pass            
        if one.SqlType.startswith("varchar"):
            str_str = str_str + one.SqlName + ", " 
            pass
        #if one.SqlType.startswith("text"):
        #    str_str = str_str + one.SqlName + ", " 
        #    pass
        if one.SqlType.endswith("text"):
            str_str = str_str + one.SqlName + ", " 
            pass
    if len(str_str) > 3:
        str_str = str_str[:-2]
    if len(int_str) > 3:
        int_str = int_str[:-2]
    if len(int_str) > 3 and len(str_str) > 3:
        return str_str + " string, " + int_str + " int "
    if len(int_str) > 3 and len(str_str) < 3:
        return int_str + " int "
    if len(int_str) < 3 and len(str_str) > 3:
        return str_str + " string"
    return ""




def get_all_golang_fileds_as_list(profile_instance):
    return_txt = []
    for one in profile_instance.ColumnsList:
        return_txt.append( one.GoName )
    return return_txt


def get_one_sql_name_by_go_name(profile_instance, go_name ):
    for one in profile_instance.ColumnsList:
        if one.GoName == go_name:
            return one.SqlName
    return ""




def get_one_go_name_by_sql_name(profile_instance, sql_name ):
    for one in profile_instance.ColumnsList:
        if one.SqlName == sql_name:
            return one.GoName
    return ""
def get_one_show_name_by_sql_name(profile_instance, sql_name ):
    for one in profile_instance.ColumnsList:
        if one.SqlName == sql_name:
            return one.ShowName
    return ""

def get_one_show_name_by_go_name(profile_instance, go_name ):
    for one in profile_instance.ColumnsList:
        if one.GoName == go_name:
            return one.ShowName
    return ""



def get_all_sql_fileds_as_list(profile_instance):
    return_txt = []
    for one in profile_instance.ColumnsList:
        return_txt.append( one.SqlName )
    return return_txt

def get_all_sql_fileds_str(profile_instance):
    return_list = get_all_sql_fileds_as_list(profile_instance)
    return_txt = ""
    #for one in return_list:
    for one in profile_instance.ColumnsList:
        return_txt = return_txt + one.SqlName + ", "
    if len(return_txt) > 3:
        return_txt = return_txt[:-2]
    return return_txt


def touch_new_file(full_path_file):
    os.system(" touch " + full_path_file)

def backup_go_file_in_curr_dir_and_touch_new_one(FullPathModelFile):
    unique_file_name = FullPathModelFile + "_" + str( time.time() ) + ".bak" 
    cp_cmd = " " + FullPathModelFile + " " + unique_file_name
    os.system( "cp " + cp_cmd )
    os.remove( FullPathModelFile )
    os.system( "touch " + FullPathModelFile )
    pass

def __get_go_file_header( contents_list ):
    return_contents = ""
    return_contents = return_contents + contents_list[0] 
    return_contents = return_contents + contents_list[1] 
    return_contents = return_contents + contents_list[2] + "\n"
    return return_contents


def __get_go_file_part( contents_list, begin_part, end_part ):
    allow_record = False
    return_contents = ""
    for line in contents_list:
        if line.startswith( begin_part ) and not allow_record:
            allow_record = True
            continue
        if line.startswith( end_part ) and allow_record:
            break
        if allow_record:
            return_contents = return_contents + line  #+ "\n"
    return return_contents


def __is_go_file_has_part( contents_list , bstr, estr ):
    b = False
    e = False
    for line in contents_list:
        if line.startswith( bstr ):
            b = True
        if line.startswith( estr ):
            e = True
    if b and e:
        return True
    else:
        return False
    return False

def is_go_file_has_auto_part( contents_list ):
    return __is_go_file_has_part( contents_list , GoTemplateAutoPartBegin, GoTemplateAutoPartEnd  )

def is_go_file_has_custom_part( contents_list ):
    return __is_go_file_has_part( contents_list , GoTemplateCustomPartBegin, GoTemplateCustomPartEnd  )




def get_go_file_header(contents_list):
    return __get_go_file_header(contents_list)
def get_go_file_auto_part( contents_list ):
    return __get_go_file_part( contents_list, GoTemplateAutoPartBegin, GoTemplateAutoPartEnd )
def get_go_file_custom_part( contents_list ):
    return __get_go_file_part( contents_list, GoTemplateCustomPartBegin, GoTemplateCustomPartEnd )



def read_model_gorp_api_file(file_path):
    contents_list = comm_funcs.get_file_content_as_list(file_path)
    pass



def check_and_create_model_domain_path(model_domain, gopath):
    """
    check the model domain path 
    if the model domain not exit , sys.exit
    if the sub directories not exits , create them.
    """
    ModelDomainPath = ModelDomainFullPath = gopath + "/src/" + model_domain
    comm_funcs.print_ok("......check_and_create_model_domain_path:" + ModelDomainPath)
    for c in ModelDomainPath:
        pass
        #print c
    if os.path.exists(ModelDomainPath):
        return True
    comm_funcs.print_error("PYTHON ERROR: ModelDomainPath not exist:" + ModelDomainPath)
    sys.exit(1)



def check_is_go_file_have_meta_flag(file_path):
    contents_list = comm_funcs.get_file_content_as_list( file_path )
    if contents_list[0].startswith("package "):
        pass
    else:
        comm_funcs.print_error("PYTHON ERROR: " + file_path + " no package ! ")
        sys.exit(1)
    if contents_list[2].startswith( GoTemplateMagicSecondLine ):
        pass
    else:
        comm_funcs.print_error("PYTHON ERROR: " + file_path + " no MagicSecondLine ! ")
        sys.exit(1)
    if is_go_file_has_auto_part( contents_list ):
        pass
    else:
        comm_funcs.print_error("PYTHON ERROR: " + file_path + " no auto part ! ")
        sys.exit(1)
    if is_go_file_has_custom_part( contents_list ):
        pass
    else:
        comm_funcs.print_error("PYTHON ERROR: " + file_path + " no custom part ! ")
        sys.exit(1)
    return True



def get_full_profile_instance_path(profile_file):
    if not profile_file.endswith(".cfg"):
        comm_funcs.print_error("ERROR: profile file extension not match cfg:" + profile_file)
        sys.exit(1)
    ModelProfileModelsPath = comm_funcs.check_and_get_go_path() + "/" + ModelProfileDirName + "/models"
    InstanceProfilePath = ModelProfileModelsPath + "/" + profile_file
    if not os.path.exists(InstanceProfilePath):
        comm_funcs.print_error("ERROR: profile file not exist:" + InstanceProfilePath)
        sys.exit(1)
    return InstanceProfilePath

def check_model_profile_exist():
    ModelProfilePath = comm_funcs.check_and_get_go_path() + "/" + ModelProfileDirName
    if not os.path.exists( ModelProfilePath + "/" +  AlreadyGeneratedModelProfileName ):
        comm_funcs.print_error("ERROR: already profile config not exist. ")
        sys.exit(1)
    return 






