# -*- coding: utf-8 –*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs
import time

import sub_gene_comm, godroid_helper



def print_ok(line):
    comm_funcs.print_ok("   api_web_module  :" + line )
def print_error(line):
    comm_funcs.print_error("   api_web_module  :" + line )


def __self_call_get_custom_part(contents_list):
    content = ""
    content = content + sub_gene_comm.GoTemplateCustomPartBegin + "\n"
    content = content + sub_gene_comm.get_go_file_custom_part( contents_list )
    content = content + sub_gene_comm.GoTemplateCustomPartEnd + "\n"
    return content


def ____self_call_get_curds(profile_instance, model_domain):
    tmplt = """

    case reflect.TypeOf(PACKAGENAME_models.MCLASSNAME{}).Name():
        iobj = new(PACKAGENAME_models.MCLASSNAME)


        
func GetEmptyCLASSNAME() *PACKAGENAME_models.MCLASSNAME {
    return new(PACKAGENAME_models.MCLASSNAME)
}

func GetOneCLASSNAME(my_id string) *PACKAGENAME_models.MCLASSNAME {
    v, _ := api_PACKAGENAME.DbGetOneCLASSNAME(my_id)
    return v
}

func FillNewCLASSNAME(url_values map[string][]string) (iobj *PACKAGENAME_models.MCLASSNAME) {
    map_values := UrlValuesToMapValue(url_values)
    tn := reflect.TypeOf(PACKAGENAME_models.MCLASSNAME{}).Name()
    ifv := findAndFillNewGobbsObj(tn, map_values)
    iobj = ifv.(*PACKAGENAME_models.MCLASSNAME)
    return
}

func SaveNewCLASSNAME(iobj *PACKAGENAME_models.MCLASSNAME) (err error, result bool) {
    if 0 == len(iobj.MyId) {
        iobj.MyId = text_string.GetUniqueId()
    }
    if err = DbGetDbm().Insert(iobj); nil == err {
        result = true
    } else {
        log.Printf("Error when save : %s", err.Error())
    }
    return
}
func SaveEditCLASSNAME(iobj *PACKAGENAME_models.MCLASSNAME) (err error, result bool) {
    if _, err = DbGetDbm().Update(iobj); nil == err {
        result = true
    }
    return
}

func RemoveCLASSNAMEByMyId(my_id string) bool {
    api_PACKAGENAME.RemoveCLASSNAMEByMyId(my_id)
    return true
}
func DeleteCLASSNAMEByMyId(my_id string) bool {
    api_PACKAGENAME.DeleteCLASSNAMEByMyId(my_id)
    return true
}

func GetAllCLASSNAME(limit, offset int) (result *[]PACKAGENAME_models.MCLASSNAME) {
    result, _ = api_PACKAGENAME.DbGetAllCLASSNAME(limit, offset)
    return
}

func EditorGetAllCLASSNAME(read_status, limit, offset int) (result *[]PACKAGENAME_models.MCLASSNAME) {
    result, _ = api_PACKAGENAME.DbGetAllCLASSNAMEListGeneral(read_status, limit, offset)
    return
}
func UpdateFieldCLASSNAME(iobj *PACKAGENAME_models.MCLASSNAME, field_name string, ivalue interface{}) *PACKAGENAME_models.MCLASSNAME {
    value_of_elem := reflect.ValueOf(iobj).Elem()
    fv := value_of_elem.FieldByName(field_name) // this name is CamelName
    setFieldByInterfaceValue(&fv, ivalue)
    return iobj
}


    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)

    return tmplt


def ____self_call_get_imports(profile_instance, model_domain):
    tmplt = """

import (
    . "MODELDOMAIN/api"
    api_PACKAGENAME "MODELDOMAIN/api/PACKAGENAME"
    PACKAGENAME_models "MODELDOMAIN/model/PACKAGENAME"
    . "MODELDOMAIN/utils/funcs"
    text_string "MODELDOMAIN/utils/text_string"
    "log"
    "reflect"
)

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)

    return tmplt
    pass

def __self_call_get_package( contents_list ):
    return sub_gene_comm.get_go_file_header(contents_list)


def generate_apiwebmodule_show_file(profile_instance, model_domain):
    """
    apiwebmodule

    """
    print_ok("begin save to apiwebmodule")
    FullPathApiWebModuleFile = godroid_helper.get_apiwebmodule_file_name_full_path(profile_instance, model_domain)
    contents_list = comm_funcs.get_file_content_as_list( FullPathApiWebModuleFile )
    part_one = __self_call_get_package(contents_list)


    #---- begin
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin

    part_package_import = ____self_call_get_imports(profile_instance, model_domain)

    part_curd = ____self_call_get_curds(profile_instance,model_domain)

    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #---- end

    
    part_auto_full = part_begin + "\n" + part_package_import + "\n" + part_curd + "\n" +  part_end


    part_custom  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_auto_full + "\n" + part_custom


    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathApiWebModuleFile )
    comm_funcs.add_to_exist_file( FullPathApiWebModuleFile  , all_file_conent  )


    pass

def generate_apiwebmodule_file(profile_instance, model_domain):
    """
    apiwebmodule
    """
    print_ok("begin generate apiwebmodule file ... ")
    generate_apiwebmodule_show_file(profile_instance, model_domain)
    pass

def __check_apiwebmodule_meta_flag(file_path):
    comm_funcs.print_ok("apiwebmodule ......begin __check_apiwebmodule_meta_flag:" + file_path)
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    print_ok("Done apiwebmodule")
    return True
    pass





