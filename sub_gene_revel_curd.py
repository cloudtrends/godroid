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
    comm_funcs.print_ok("   revel_curd_funcs  :" + line )
def print_error(line):
    comm_funcs.print_error("   revel_curd_funcs  :" + line )



def ____self_call_get_curds(profile_instance, model_domain):
    tmplt = """


func init() {

    //--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- Mxxxxxxxxx
    FuncGetEmptyCLASSNAME := func() *PACKAGENAME_models.MCLASSNAME {
        return GetEmptyCLASSNAME()
    }
    r.TemplateFuncs["GetEmptyCLASSNAME"] = FuncGetEmptyCLASSNAME
    //---
    FuncGetOneCLASSNAME := func(my_id string) *PACKAGENAME_models.MCLASSNAME {
        return GetOneCLASSNAME(my_id)
    }
    r.TemplateFuncs["GetOneCLASSNAME"] = FuncGetOneCLASSNAME
    //---
    FuncFillNewCLASSNAME := func(map_values map[string][]string) *PACKAGENAME_models.MCLASSNAME {
        return FillNewCLASSNAME(map_values)
    }
    r.TemplateFuncs["FillNewCLASSNAME"] = FuncFillNewCLASSNAME
    //---
    FuncSaveNewCLASSNAME := func(iobj *PACKAGENAME_models.MCLASSNAME) (curd urltoaction.CurdResult) {
        if err, ok := SaveNewCLASSNAME(iobj); err == nil && ok {
            curd.IsOk = true
        } else {
            curd.IsOk = false
            curd.Error = err
        }
        return
    }
    r.TemplateFuncs["SaveNewCLASSNAME"] = FuncSaveNewCLASSNAME
    //---
    FuncSaveEditCLASSNAME := func(iobj *PACKAGENAME_models.MCLASSNAME) (curd urltoaction.CurdResult) {
        if err, ok := SaveEditCLASSNAME(iobj); err == nil && ok {
            curd.IsOk = true
        } else {
            curd.IsOk = false
            curd.Error = err
        }
        return
    }
    r.TemplateFuncs["SaveEditCLASSNAME"] = FuncSaveEditCLASSNAME
    //---
    FuncGetAllCLASSNAME := func(limit, offset int) *[]PACKAGENAME_models.MCLASSNAME {
        return GetAllCLASSNAME(limit, offset)
    }
    r.TemplateFuncs["GetAllCLASSNAME"] = FuncGetAllCLASSNAME
    //---
    FuncSetCLASSNAME := func(iobj *PACKAGENAME_models.MCLASSNAME, field_name string, str_value interface{}) *PACKAGENAME_models.MCLASSNAME {
        return UpdateFieldCLASSNAME(iobj, field_name, str_value)
    }
    r.TemplateFuncs["UpdateFieldCLASSNAME"] = FuncSetCLASSNAME
    //---
    FuncRemoveCLASSNAMEByMyId := func(my_id string) bool {
        return RemoveCLASSNAMEByMyId(my_id)
    }
    r.TemplateFuncs["RemoveCLASSNAMEByMyId"] = FuncRemoveCLASSNAMEByMyId
    //---
    FuncDeleteCLASSNAMEByMyId := func(my_id string) bool {
        return DeleteCLASSNAMEByMyId(my_id)
    }
    r.TemplateFuncs["DeleteCLASSNAMEByMyId"] = FuncDeleteCLASSNAMEByMyId
    //---
    //--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- THE END
    self_custom_CLASSNAME()
}



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)

    return tmplt



def ____self_call_get_imports(profile_instance, model_domain):
    tmplt = """

import (
    . "MODELDOMAIN/api/web/gobbs"
    "MODELDOMAIN/framework/urltoaction"
    PACKAGENAME_models "MODELDOMAIN/model/PACKAGENAME"
    r "github.com/robfig/revel"
)



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)

    return tmplt
    pass



def __self_call_get_package( contents_list ):
    return sub_gene_comm.get_go_file_header(contents_list)

def __self_call_get_custom_part(contents_list):
    """
    if first time we should add empty func: func self_routes_routes() 


    """
    content = ""
    content = content + sub_gene_comm.GoTemplateCustomPartBegin + "\n"
    content_custom_part_tmp = sub_gene_comm.get_go_file_custom_part( contents_list )
    if len( content_custom_part_tmp ) < 6 :
        content_custom_part_tmp = """
        func self_custom_CLASSNAME(){
        
        }        
        """

    content = content + content_custom_part_tmp
    content = content + sub_gene_comm.GoTemplateCustomPartEnd + "\n"

    return content



def generate_revelcurdfuncs_show_file(profile_instance, model_domain):
    """
    revelcurdfuncs
    """
    print_ok("begin save to revelcurdfuncs")
    FullPathRevelCurdFuncsFile = godroid_helper.get_revelcurdfuncs_file_name_full_path(profile_instance, model_domain) 
    contents_list = comm_funcs.get_file_content_as_list( FullPathRevelCurdFuncsFile )
    part_one = __self_call_get_package(contents_list)


    #---- begin
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin

    part_package_import = ____self_call_get_imports(profile_instance,model_domain)

    part_curd = ____self_call_get_curds(profile_instance , model_domain)

    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #---- end

    part_auto_full = part_begin + "\n" + part_package_import + "\n" + part_curd + "\n" +  part_end

    part_custom  = __self_call_get_custom_part(contents_list)
    part_custom = part_custom.replace("CLASSNAME", profile_instance.ClassName)

    all_file_conent = part_one + "\n" + part_auto_full + "\n" + part_custom

    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathRevelCurdFuncsFile )
    comm_funcs.add_to_exist_file( FullPathRevelCurdFuncsFile  , all_file_conent  )







def generate_revelcurdfuncs_file(profile_instance, model_domain):
    """
    revelcurdfuncs
    """
    generate_revelcurdfuncs_show_file(profile_instance, model_domain)
    pass



def __check_revelcurdfuncs_meta_flag(file_path):
    comm_funcs.print_ok("......begin __check_revelcurdfuncs_meta_flag:" + file_path)
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    return True
    pass

