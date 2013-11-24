# -*- coding: utf-8 –*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs


import sub_gene_comm, godroid_helper




def __self_call_get_package( contents_list ):
    return sub_gene_comm.get_go_file_header(contents_list)

def __self_call_get_custom_part(contents_list):
    content = ""
    content = content + sub_gene_comm.GoTemplateCustomPartBegin + "\n"
    content = content + sub_gene_comm.get_go_file_custom_part( contents_list )
    content = content + sub_gene_comm.GoTemplateCustomPartEnd + "\n"
    return content


def ____self_call_get_method_select_one(profile_instance, model_domain):
    tmplt = """


func DbGetOneCLASSNAME(id string) (*PACKAGENAME_models.MCLASSNAME, bool) {
    var item *PACKAGENAME_models.MCLASSNAME
    rb := false
    var results []interface{}
    sql_str := " SELECT * FROM  " + PACKAGENAME_models.CLASSNAMETableName + "  WHERE XXXXXXX "
    results, rb2 := ApiG_rawselect(news_models.MCLASSNAME{}, sql_str, id)
    if rb2 {
        if len(results) > 0 {
            item = results[0].(*PACKAGENAME_models.MCLASSNAME)
            rb = true
        }
    }
    return item, rb
}

    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt

    pass

def ____self_call_get_method_save_new(profile_instance, model_domain):
    """
    """
    tmplt = """

func SaveNewCLASSNAME( CONDI_FIELDS ) bool {
    //my_id := text_string.GetUniqueId()
    obj := PACKAGENAME_models.MCLASSNAME{

        FIELDS_VALUE

    }
    err := DbGetDbm().Insert(&obj)
    if err != nil {
        log.Println("insert new record error:")
        log.Println(err)
        return false
    }
    return true
}


    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    condi_fields = sub_gene_comm.get_all_sql_fileds_params_str(profile_instance)
    tmplt = tmplt.replace("CONDI_FIELDS" , condi_fields )
    fileds_value_pair = ""
    for one in profile_instance.ColumnsList:
        tmp_one_fields = one.GoName + "    :    " + one.SqlName + ", "
        fileds_value_pair = fileds_value_pair + tmp_one_fields + "\n"
    tmplt = tmplt.replace("FIELDS_VALUE", fileds_value_pair)

    return tmplt
    pass



def ____self_call_get_method_get_all(profile_instance, model_domain):
    tmplt = """

func DbGetAllCLASSNAMEList(CONDI_FIELDS   , page_num, offset int) ([]*PACKAGENAME_models.MCLASSNAME, bool) {
    var items []*PACKAGENAME_models.MCLASSNAME
    rb := false
    var results []interface{}
    rb2 := false
    var sql_str string
    sql_str = "SELECT * FROM " + PACKAGENAME_models.CLASSNAMETableName + " WHERE XXXXXX "
    results, rb2 = ApiG_rawselect(PACKAGENAME_models.MCLASSNAME{}, sql_str, XXXXXX )
    if rb2 {
        for _, one := range results {
            items = append(items, one.(*PACKAGENAME_models.MCLASSNAME))
        }
        rb = true
    }
    return items, rb
}

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    #condi_fields = sub_gene_comm.get_all_sql_fileds_str(profile_instance)
    condi_fields = sub_gene_comm.get_all_sql_fileds_params_str(profile_instance)
    tmplt = tmplt.replace("CONDI_FIELDS" , condi_fields )
    return tmplt
    pass


def ____self_call_get_method_isexits(profile_instance, model_domain):
    tmplt = """

func IsCLASSNAMEExist( CONDI_FIELDS ) bool {
    sql_str := " SELECT count( XXXXXX ) Count FROM " + PACKAGENAME_models.CLASSNAMETableName + " where  XXXXXX XXXXXXX "
    var results []interface{}
    results, rb2 := ApiG_rawselect(fake_models.MTotalCount{}, sql_str, XXXXXX, XXXXXX, XXXXXX)
    num := 0
    if rb2 {
        if len(results) > 0 {
            fake_obj := results[0].(*fake_models.MTotalCount)
            num = fake_obj.Count
        }
    }
    if num > 0 {
        return true
    }
    return false
}

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    #condi_fields = sub_gene_comm.get_all_sql_fileds_str(profile_instance)
    condi_fields = sub_gene_comm.get_all_sql_fileds_params_str(profile_instance)
    tmplt = tmplt.replace("CONDI_FIELDS" , condi_fields )



    return tmplt
    pass




def __self_call_get_stands_methods(profile_instance, model_domain):
    isexists = ____self_call_get_method_isexits(profile_instance, model_domain)
    getall = ____self_call_get_method_get_all(profile_instance, model_domain)
    savenew = ____self_call_get_method_save_new(profile_instance, model_domain)
    selectone = ____self_call_get_method_select_one(profile_instance, model_domain)

    all_methods = isexists + getall + savenew + selectone
    return all_methods

def __self_call_get_import(profile_instance, model_domain):
    tmplt = """
    
import (
    "github.com/coopernurse/gorp"
    . "MODELDOMAIN/api"
    "log"
    PACKAGENAME_models "MODELDOMAIN/model/PACKAGENAME"
    //fake_models "MODELDOMAIN/model/fake"
    //time_utils "MODELDOMAIN/utils/time"
    //text_string "MODELDOMAIN/utils/text_string"
    . "golanger.com/middleware"
    
)


    """
    tmplt = tmplt.replace("PACKAGENAME" , profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    return tmplt
    pass

def generate_api_file(profile_instance, model_domain):
    """
    first , save contents which outside of meta flag
    then , generate new content 
    third , combine them and generate new file
    """
    FullPathApiFile = godroid_helper.get_api_file_name_full_path(profile_instance, model_domain)
    contents_list = comm_funcs.get_file_content_as_list( FullPathApiFile )
    part_one = __self_call_get_package(contents_list)


    comm_funcs.print_ok( "api part one:" + part_one )

    part_begin = sub_gene_comm.GoTemplateAutoPartBegin
    part_two =  __self_call_get_stands_methods(profile_instance, model_domain)
    #()
    part_three = ""
    #(profile_instance, model_domain)
    part_four = ""
    part_five = ""

    part_end = sub_gene_comm.GoTemplateAutoPartEnd

    part_six  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_begin + "\n" + part_two + "\n" + part_three + "\n" + part_four + "\n" + part_five + "\n" + part_end + "\n" + part_six
    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathApiFile )
    comm_funcs.print_ok("begin save to api:" + FullPathApiFile)
    comm_funcs.add_to_exist_file( FullPathApiFile  , all_file_conent  )
    pass

def __check_api_meta_flag( file_path ):
    comm_funcs.print_ok("......begin __check_api_meta_flag:" + file_path)
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    return True

    