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


def __self_call_get_package( contents_list ):
    return sub_gene_comm.get_go_file_header(contents_list)

def __self_call_get_table_name_const(contents_list, profile_instance):
    content = """
    const (
        CLASSNAMECONSTTableName string = "TABLENAMECONST" //----------MUST CHANGE
    )
    """
    content = content.replace("TABLENAMECONST", profile_instance.TableName)
    content = content.replace("CLASSNAMECONST", profile_instance.ClassName)
    return content

def __self_call_get_class(profile_instance):
    content = ""
    content = content + "type M"+ profile_instance.ClassName +" struct {" + "\n"
    content = content + "    Id         int" + "\n"
    for col in profile_instance.ColumnsList:
        content = content + "    "+ col.GoName +"         "+  col.GoType +"\n"
    content = content + "}" + "\n"
    #Id         int
    #MyId       string
    return content


def __self_call_get_GetColumnsMap(profile_instance):
    """
    """
    content = ""
    content = content + "func (m M"+ profile_instance.ClassName +") GetColumnsMap() map[string]string {" + "\n"
    content = content + "    var columns_map map[string]string" + "\n"
    content = content + "    //columns_map[\"\"] = \"\"" + "\n"
    content = content + "    columns_map = make(map[string]string)" + "\n"
    content = content + "    columns_map[\"id\"] = \"int\"" + "\n"
    for col in profile_instance.ColumnsList:
        content = content + "    columns_map[\"" + col.SqlName + "\"] = \""+ col.SqlType +"\"" + "\n"
    content = content + "    return columns_map" + "\n"
    content = content + "}" + "\n"
    return content



def __self_call_get_GetGorpRenameMap(profile_instance):
    """
    """
    content = ""
    content = content + "func (m M"+ profile_instance.ClassName +") GetGorpRenameMap() map[string]string {" +  "\n"
    content = content + "    var gorp_rename_map map[string]string" +  "\n"
    content = content + "    //gorp_rename_map[\"\"] = \"\"" +  "\n"
    content = content + "    gorp_rename_map = make(map[string]string)" +  "\n"
    content = content + "    gorp_rename_map[\"Id\"] = \"id\"" +  "\n"
    for col in profile_instance.ColumnsList:
        content = content + "    gorp_rename_map[\""+ col.GoName +"\"] = \""+ col.SqlName +"\"" +  "\n"    
    
    content = content + "    return gorp_rename_map" +  "\n"
    content = content + "}" +  "\n"
    return content



def __self_call_get_custom_part(contents_list):
    content = ""
    content = content + sub_gene_comm.GoTemplateCustomPartBegin + "\n"
    content = content + sub_gene_comm.get_go_file_custom_part( contents_list )
    content = content + sub_gene_comm.GoTemplateCustomPartEnd + "\n"
    return content




def generate_model_class_file(profile_instance, model_domain):
    FullPathModelFile = godroid_helper.get_model_class_file_name_full_path(profile_instance, model_domain)
    contents_list = comm_funcs.get_file_content_as_list( FullPathModelFile )
    part_one = __self_call_get_package(contents_list)
    comm_funcs.print_ok( "class part one:" + part_one )
    #---- begin
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin
    part_two = __self_call_get_table_name_const(contents_list, profile_instance)
    part_three = __self_call_get_class(profile_instance)
    part_four = __self_call_get_GetColumnsMap(profile_instance)
    part_five = __self_call_get_GetGorpRenameMap(profile_instance)
    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #---- end 
    part_six  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_begin + "\n" + part_two + "\n" + part_three + "\n" + part_four + "\n" + part_five + "\n" + part_end + "\n" + part_six
    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathModelFile )
    comm_funcs.add_to_exist_file( FullPathModelFile  , all_file_conent  )
    pass


def __check_model_meta_flag( file_path ):
    comm_funcs.print_ok("......begin __check_model_meta_flag:" + file_path)
    # if check failed then sys exit
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    return True