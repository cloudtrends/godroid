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


def __self_call_get_import(contents_list, profile_instance,model_domain):
    tmplt="""
    import (
        "log"
        "github.com/coopernurse/gorp"
        . "golanger.com/middleware"
        funcs_utils "MODELDOMAIN/utils/funcs"
        mysql_utils "MODELDOMAIN/utils/mysql"
        sqlite_utils "MODELDOMAIN/utils/sqlite"
    )
    """
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    return tmplt
    pass

def __self_call_get_class_def(contents_list, profile_instance):
    tmplt="""
    
    type MGorpCLASSNAME struct {
        sqlite_utils.SqliteUtils
        mysql_utils.MysqlUtils
    }

    """
    tmplt = tmplt.replace( "CLASSNAME" , profile_instance.ClassName )
    return tmplt


def __self_call_get_func_for_sql_tri_pairs(contents_list, profile_instance):
    tmplt = """

func (c MGorpCLASSNAME) Sqlite_sql_tri_pairs_for_CLASSNAME(db_type string) ([]string, funcs_utils.DFuncs, map[string]string) {

    var tables []string
    funcs_call := funcs_utils.NewDFuncs(100)
    check_funcs := make(map[string]interface{})
    maps_funcs_table_name := make(map[string]string)
    //--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    table_variable_name := TABLENAME
    tables = append(tables, table_variable_name)

    check_funcs_key := "check_columns_" + table_variable_name
    check_funcs[check_funcs_key] = func(t_name string) {

        xxxxx := MCLASSNAME{}
        columns_map := xxxxx.GetColumnsMap()

        if "sqlite" == db_type {
            c.SqliteCheck_clumns_for_map(t_name, columns_map)
        } else {
            c.MySQLCheck_clumns_for_map(t_name, columns_map)
        }
    }
    maps_funcs_table_name[table_variable_name] = check_funcs_key
    //--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    //--- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

    for k, v := range check_funcs {
        err := funcs_call.Bind(k, v)
        if err != nil {
            log.Println(err)
        }
    }
    return tables, funcs_call, maps_funcs_table_name
}


    """
    
    tmplt = tmplt.replace( "CLASSNAME"  , profile_instance.ClassName)
    tmplt = tmplt.replace( "TABLENAME"  , profile_instance.ClassName + "TableName")


    return tmplt



def __self_call_get_gorp_map(contents_list, profile_instance):
    tmplt="""


func (c MGorpCLASSNAME) InitGorpMapForCLASSNAME() {
    name := "InitGorpMapForCLASSNAME"
    log.Println("begin init   " + name)
    dbm_raw := Middleware.Get("dbm")
    dbm := dbm_raw.(*gorp.DbMap)

        //<------------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- MUST CHANGE
        table_name := TABLENAME // <------------ --- --- --- --- --- --- --- MUST CHANGE
        //<------------ --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- MUST CHANGE
        table_one := dbm.AddTableWithName(MCLASSNAME{}, table_name).SetKeys(true, "Id")


    obj := MCLASSNAME{}
    gorp_map := obj.GetGorpRenameMap()
    for k, v := range gorp_map {
        table_one.ColMap(k).Rename(v)
    }

}


    """
    tmplt = tmplt.replace( "CLASSNAME"  , profile_instance.ClassName)
    tmplt = tmplt.replace( "TABLENAME"  , profile_instance.ClassName + "TableName")
    return tmplt



def generate_funcs_of_gorp_file(profile_instance, model_domain):
    FullPathFuncsOfGorpFile = godroid_helper.get_model_funcs_of_gorp_file_name_full_path(profile_instance, model_domain)
    contents_list = comm_funcs.get_file_content_as_list( FullPathFuncsOfGorpFile )
    part_one = __self_call_get_package(contents_list)
    comm_funcs.print_ok( "gorp funcs part one:" + part_one )
    #
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin
    #
    part_two = __self_call_get_import(contents_list, profile_instance, model_domain)
    part_three = __self_call_get_class_def(contents_list, profile_instance)
    part_four = __self_call_get_func_for_sql_tri_pairs(contents_list, profile_instance)
    part_five = __self_call_get_gorp_map(contents_list, profile_instance)
    #
    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #
    part_six  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_begin + "\n" + part_two + "\n" + part_three + "\n" + part_four + "\n" + part_five + "\n" + part_end + "\n" + part_six
    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathFuncsOfGorpFile )
    comm_funcs.print_ok("begin save to gorp:" + FullPathFuncsOfGorpFile)
    comm_funcs.add_to_exist_file( FullPathFuncsOfGorpFile  , all_file_conent  )
    pass


def __check_funcs_meta_flag( file_path ):
    comm_funcs.print_ok("......begin __check_funcs_meta_flag:" + file_path)
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    return True
    

