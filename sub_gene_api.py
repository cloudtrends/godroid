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


def ____self_call_method_save_edit(profile_instance, model_domain):
    tmplt = """

func SaveEdit(obj *PACKAGENAME_models.MCLASSNAME) bool {
    DbGetDbm().Update(obj)
    return true
}

    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt

def ____self_call_get_method_remove_by_my_id(profile_instance, model_domain):
    tmplt = """


func RemoveByMyId(my_id string) {
    var sql_str string
    sql_str = " DELETE FROM " + PACKAGENAME_models.CLASSNAMETableName + "   WHERE my_id = ? "
    ApiG_rawexec(sql_str, my_id)
}



    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt


def ____self_call_get_method_delete_by_my_id(profile_instance, model_domain):
    tmplt = """

func DeleteByMyId(my_id string) {
    var sql_str string
    sql_str = " UPDATE " + PACKAGENAME_models.CLASSNAMETableName + " SET read_status = -1 WHERE my_id = ? "
    ApiG_rawexec(sql_str, my_id)
}

    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt

def ____self_call_get_method_select_one(profile_instance, model_domain):
    tmplt = """


func DbGetOneCLASSNAME(my_id string) (*PACKAGENAME_models.MCLASSNAME, bool) {
    var item *PACKAGENAME_models.MCLASSNAME
    rb := false
    var results []interface{}
    sql_str := " SELECT * FROM  " + PACKAGENAME_models.CLASSNAMETableName + "  WHERE 1=1 "
    sql_str = sql_str + "  "
    sql_str = sql_str + " AND my_id = ? "
    results, rb2 := ApiG_rawselect(PACKAGENAME_models.MCLASSNAME{}, sql_str, my_id)
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

/**
 ------------- HOW TO USE


    func (c ControllerXXXX) AddSaveCLASSNAME(CONDIFIELDS_USER_INPUT) revel.Result {
        //read_status := 1
        //user_id := ""
        //ip := RevelGetIpAddress(c.Request)
        //my_id := ""
        //a, b := text_string.GetCurrDateTime()
        //input_date := a
        //input_time := b
        //input_datetime := a + " " + b
        //input_time_seq := text_string.GetCurrentSeconds()

        api_PACKAGENAME.SaveNewCLASSNAME(CONDI_FIELDS)
        return c.Redirect(routes.ControllerXXXX.List(flxx_cat_id))
    }

*/
func SaveNewCLASSNAME( CONDI_FIELDS ) bool {
    my_id = text_string.GetUniqueId()
    //GetShortUniqueId
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
    #
    condi_fields_user_input = condi_fields
    #condi_fields_user_input = condi_fields_user_input.replace("","")
    condi_fields_user_input = condi_fields_user_input.replace("input_time_seq","")
    condi_fields_user_input = condi_fields_user_input.replace("input_datetime","")
    condi_fields_user_input = condi_fields_user_input.replace("input_time","")
    condi_fields_user_input = condi_fields_user_input.replace("input_date","")
    condi_fields_user_input = condi_fields_user_input.replace("my_id","")
    condi_fields_user_input = condi_fields_user_input.replace("ip","")
    condi_fields_user_input = condi_fields_user_input.replace("user_id","")
    condi_fields_user_input = condi_fields_user_input.replace("read_status","")




    tmplt = tmplt.replace("CONDIFIELDS_USER_INPUT" , condi_fields_user_input )

    fileds_value_pair = ""
    for one in profile_instance.ColumnsList:
        tmp_one_fields = one.GoName + "    :    " + one.SqlName + ", "
        fileds_value_pair = fileds_value_pair + tmp_one_fields + "\n"
    tmplt = tmplt.replace("FIELDS_VALUE", fileds_value_pair)

    return tmplt
    pass



def ____self_call_get_method_get_all(profile_instance, model_domain):
    tmplt = """

func DbGetAllCLASSNAMEList(CONDI_FIELDS   , limit, offset int) ([]*PACKAGENAME_models.MCLASSNAME, bool) {
    var items []*PACKAGENAME_models.MCLASSNAME
    rb := false
    var results []interface{}
    rb2 := false
    var sql_str string
    sql_str = "SELECT * FROM " + PACKAGENAME_models.CLASSNAMETableName + " WHERE 1 = 1 "
    sql_str = sql_str + ""
    sql_str = sql_str + " AND read_status = ? "
    sql_str = sql_str + " ORDER BY ID DESC "
    sql_str = sql_str + " LIMIT ? OFFSET ? "
    results, rb2 = ApiG_rawselect(PACKAGENAME_models.MCLASSNAME{}, sql_str , limit, offset )
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

def ____self_call_get_imports(profile_instance, model_domain):
    tmplt = """


import (
    //"github.com/coopernurse/gorp"
    . "MODELDOMAIN/api"
    fake_models "MODELDOMAIN/model/fake"
    PACKAGENAME_models "MODELDOMAIN/model/PACKAGENAME"
    text_string "MODELDOMAIN/utils/text_string"
    //"github.com/coopernurse/gorp"
    //. "golanger.com/middleware"
    "log"
    //mysql_utils "MODELDOMAIN/utils/mysql"
    //sqlite_utils "MODELDOMAIN/utils/sqlite"
)


    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)

    return tmplt
    pass


def ____self_call_get_method_isexits(profile_instance, model_domain):
    tmplt = """

func IsCLASSNAMEExist( CONDI_FIELDS ) bool {
    sql_str := " SELECT count( XXXXXX ) Count FROM " + PACKAGENAME_models.CLASSNAMETableName + " where  XXXXXX XXXXXXX "
    var results []interface{}
    results, rb2 := ApiG_rawselect(fake_models.MTotalCount{}, sql_str )
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


def ____self_call_only_reference(profile_instance, model_domain):
    tmplt = """

/*
//----------------------------- BELOW CODE ONLY FOR REFERENCE 


//-------------------  in sql init


PACKAGENAME_models "DOMAINMODEL/model/PACKAGENAME"

PACKAGENAME_models.MGorpCLASSNAME
c.InitGorpMapForCLASSNAME()

//
tables, funcs_call, maps_funcs_table_name = c.Sqlite_sql_tri_pairs_for_CLASSNAME("sqlite")
c.CheckSqlite(tables, funcs_call, maps_funcs_table_name)

    //
    tables, funcs_call, maps_funcs_table_name = c.Sqlite_sql_tri_pairs_for_CLASSNAME("mysql")
    c.CheckMySQL(tables, funcs_call, maps_funcs_table_name)
    

//-------------------
import (
    api_PACKAGENAME "DOMAINMODEL/api/PACKAGENAME"
    PACKAGENAME_models "DOMAINMODEL/model/PACKAGENAME"
    r "github.com/robfig/revel"
    "log"
)

func init() {
 
    //r.TemplateFuncs["ViewGetAllCLASSNAMEList"] = func(read_status int, limit, offset int) []*PACKAGENAME_models.MCLASSNAME {
    //    v, rb := api_PACKAGENAME.DbGetAllCLASSNAMEList(read_status, limit, offset)
    //    if !rb {
    //        log.Println("Error when  DbGetAllCLASSNAMEList")
    //    }
    //    return v
    //}


    r.TemplateFuncs["ViewGetOneEmptyCLASSNAMEObj"] = func() *PACKAGENAME_models.MCLASSNAME {
        var obj *PACKAGENAME_models.MCLASSNAME
        obj = new(PACKAGENAME_models.MCLASSNAME)
        return obj
    }


    r.TemplateFuncs["ViewGetOneCLASSNAME"] = func(my_id string) *PACKAGENAME_models.MCLASSNAME {
        v, rb := api_PACKAGENAME.DbGetOneCLASSNAME(my_id)
        if !rb {
            log.Println("Error when  DbGetOneCLASSNAME")
        }
        return v
    }

}

 

    """
    tmplt = tmplt.replace("DOMAINMODEL", model_domain)
    
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    return tmplt


def ____self_call_method_html_code_template(profile_instance, model_domain):
    tmplt_input = """
<tr >
<td>SHOWNAME</td><td><input type="text" length="80" size="30" name="SQLNAME" value="{{ $one_item.GONAME }}"></td>
</tr>

    """
    tmplt_show = """
<tr ><td >SHOWNAME</td><td>
    {{ $one_item.GONAME }}
</td></tr>

    """
    tmplt_input_all = ""
    for one in sub_gene_comm.get_all_sql_fileds_as_list(profile_instance):
        tmp_str = tmplt_input.replace( "SQLNAME" , one )
        tmp_str = tmp_str.replace("GONAME", sub_gene_comm.get_one_go_name_by_sql_name(profile_instance,  one))
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_sql_name(profile_instance,  one))

        tmplt_input_all = tmplt_input_all + tmp_str

    tmplt_show_all = ""
    for one in sub_gene_comm.get_all_golang_fileds_as_list(profile_instance):
        tmp_str = tmplt_show.replace( "GONAME" , one  )
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_go_name(profile_instance,  one))
        tmplt_show_all = tmplt_show_all + tmp_str
    return  "/*  HTML REFERENCE \n"+ tmplt_input_all + "\n\n\n\n\n\n\n\n\n\n\n\n" +  tmplt_show_all  + "\n*/"
    pass

def __self_call_get_stands_methods(profile_instance, model_domain):
    imports = ____self_call_get_imports(profile_instance, model_domain)
    isexists = ____self_call_get_method_isexits(profile_instance, model_domain)
    getall = ____self_call_get_method_get_all(profile_instance, model_domain)
    savenew = ____self_call_get_method_save_new(profile_instance, model_domain)
    selectone = ____self_call_get_method_select_one(profile_instance, model_domain)
    deleteone = ____self_call_get_method_delete_by_my_id(profile_instance, model_domain)
    removeone = ____self_call_get_method_remove_by_my_id(profile_instance, model_domain)
    edit_save = ____self_call_method_save_edit(profile_instance, model_domain)
    only_reference = ____self_call_only_reference(profile_instance, model_domain)
    html_template = ____self_call_method_html_code_template(profile_instance, model_domain)

    all_methods = imports + isexists + getall + savenew + selectone + deleteone + removeone + edit_save + only_reference + html_template
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

    
