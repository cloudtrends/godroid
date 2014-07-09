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



def __self_call_get_admin_packages_part(profile_instance, model_domain):
    tmplt = """

import (
    //"domolo.com/gobbs/dcontroller"
    //api_PACKAGENAME "domolo.com/api/PACKAGENAME"
    //PACKAGENAME_models "domolo.com/model/PACKAGENAME"
    "github.com/robfig/revel"
    "log"
    "runtime"
    . "domolo.com/revel_helper"
)

    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt
    pass


def __self_call_get_packages_part(profile_instance, model_domain):
    tmplt = """

import (
    //"domolo.com/gobbs/dcontroller"
    //api_PACKAGENAME "domolo.com/api/PACKAGENAME"
    //PACKAGENAME_models "domolo.com/model/PACKAGENAME"
    "github.com/robfig/revel"
    "log"
    . "domolo.com/drevel"
)


    """
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt
    pass


def __self_call_get_admin_CURD_part(profile_instance, model_domain):
    tmplt = """

/*
func (c CONTROLLERNAME) ApiV1Add(user_name, api_token,  xxx string) revel.Result {
    if !c.IsApiUserValid(user_name, api_token) {
        log.Println("Error user name is empty")
        return c.RenderText("ok ok ok")
    }
    c.AddSaveCLASSNAME(xxxx)
    return c.RenderText("ok")
}
*/

func (c CONTROLLERNAME) GuanliIndex() revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin index")
    return c.RenderTemplate(GetAdminsTemplateFile("HTMLPACKAGEDIRNAME/index.html"))
}

func (c CONTROLLERNAME) GuanliList() revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin list")
    return c.RenderTemplate(GetAdminsTemplateFile("HTMLPACKAGEDIRNAME/list.html"))
}

func (c CONTROLLERNAME) GuanliAdd() revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin add")

    return c.RenderTemplate(GetAdminsTemplateFile("HTMLPACKAGEDIRNAME/add.html"))
}

func (c CONTROLLERNAME) GuanliAddSave() revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin add save")
    return c.Redirect("/")
}

func (c CONTROLLERNAME) GuanliEdit(my_id string) revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin edit")
    return c.RenderTemplate(GetAdminsTemplateFile("HTMLPACKAGEDIRNAME/edit.html"))
}

func (c CONTROLLERNAME) GuanliEditSave() revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    var err error
    if err != nil {
        funcName, file, line, ok := runtime.Caller(0)
        if ok {
            log.Println("Func Name=" + runtime.FuncForPC(funcName).Name())
            log.Println("file: %s    line=%d", file, line)
            log.Println("%s %s %s", c.Request.RemoteAddr, c.Request.Method, c.Request.URL)

        }
    }
    log.Println("begin editsave")
    return c.Redirect("/")
}

func (c CONTROLLERNAME) GuanliDelete(my_id string) revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin delete")
    return c.Redirect("/")
}
func (c CONTROLLERNAME) GuanliRemove(my_id string) revel.Result {
    if !c.CheckIsEditorLogin() {
        c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin remove")
    return c.Redirect("/")
}

    """
    dir_str = ""
    is_find, dir_list = godroid_helper.get_package_dir_list_from_package_name(profile_instance, model_domain)
    if is_find:
        for one in dir_list:
            dir_str = dir_str + one +"/" 
        dir_str = dir_str[:-1]
        tmplt = tmplt.replace("HTMLPACKAGEDIRNAME", dir_str)
        pass
    else:
        tmplt = tmplt.replace("HTMLPACKAGEDIRNAME", profile_instance.PackageName)
        pass
    tmplt = tmplt.replace("CONTROLLERNAME", profile_instance.ControlCalssName)
    #tmplt = tmplt.replace("HTMLPACKAGEDIRNAME", profile_instance.PackageName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    return tmplt

def __self_call_get_admin_auto_empty_test_part(profile_instance, model_domain):
    tmplt = """

    func CONTROLLERNAME_admin_Test(){

    }

    """
    tmplt = tmplt.replace("CONTROLLERNAME", profile_instance.ControlCalssName)
    return tmplt

def __self_call_get_auto_empty_test_part(profile_instance, model_domain):
    tmplt = """

    func CONTROLLERNAME_Test(){

    }

    """
    tmplt = tmplt.replace("CONTROLLERNAME", profile_instance.ControlCalssName)
    return tmplt
    pass

def __self_call_get_CURD_part(profile_instance, model_domain):
    tmplt = """

type CONTROLLERNAME struct {
    //Application
    GobbsApp  Module Name
}

func (c CONTROLLERNAME)  Index() revel.Result {
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin index")
    return c.RenderTemplate(GetTemplateFile("HTMLPACKAGEDIRNAME/index.html"))
}

func (c CONTROLLERNAME)  List() revel.Result {
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin list")
    return c.RenderTemplate(GetTemplateFile("HTMLPACKAGEDIRNAME/list.html"))
}
/*
func (c CONTROLLERNAME)  Add() revel.Result {
    if !CheckCommonUserIsLogin(){
        log.Println("user is not login , so redirect.")
        return c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin add")

    return c.RenderTemplate(GetTemplateFile("HTMLPACKAGEDIRNAME/add.html"))
}

func (c CONTROLLERNAME)  AddSave() revel.Result {
    if !CheckCommonUserIsLogin(){
        log.Println("user is not login , so redirect.")
        return c.Redirect("/")
    }

    c.AddSaveCLASSNAME(CONDIFIELDS_USER_INPUT)
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    log.Println("begin add save")
    return c.Redirect("/")
}


    func (c CONTROLLERNAME) AddSaveCLASSNAME(CONDIFIELDS_USER_INPUT)  {
        //dpage := c.GetMBody()
        //c.Validation.Required(title).Message("标题不能为空")
        //c.Validation.Required(content).Message("内容不能为空")

        //c.Validation.MinSize(title, 4).Message("标题最短为4个字符")
        //if c.Validation.HasErrors() {
        //    c.Validation.Keep()
        //    c.FlashParams()
        //    c.Flash.Error("信息不正确")

        //    c.RenderArgs["dpage"] = dpage
        //    log.Println("empty user input , so redirect to bbs ")
            ////return c.Redirect(c.NewAnnoymousToBbs)
            ////return c.Redirect("/go/post_to_flxxpro.html")
        //    return c.Redirect(routes.CONTROLLERNAME.XXXXXXXXXXX(""))

        ////}
        //title = template.HTMLEscapeString(title)
        //title = strings.TrimSpace(title)


        //read_status := 1
        //user_id := ""
        //ip := RevelGetIpAddress(c.Request)
        //my_id := ""
        //a, b := text_string.GetCurrDateTime()
        //input_date := a
        //input_time := b
        //input_datetime := a + " " + b
        //input_time_seq := text_string.GetCurrentSeconds()
        //GetUniqueId

        api_PACKAGENAME.SaveNewCLASSNAME(CONDI_FIELDS)
        //c.RenderArgs["dpage"] = dpage
        //return c.Redirect(routes.CONTROLLERNAME.List())
    }

func (c CONTROLLERNAME)  Edit(my_id string) revel.Result {
    if !CheckCommonUserIsLogin(){
        log.Println("user is not login , so redirect.")
        return c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin edit")
    return c.RenderTemplate(GetTemplateFile("HTMLPACKAGEDIRNAME/edit.html"))
}

func (c CONTROLLERNAME)  EditSave() revel.Result {
    if !CheckCommonUserIsLogin(){
        log.Println("user is not login , so redirect.")
        return c.Redirect("/")
    }
    dpage := c.GetMBody()
    c.RenderArgs["dpage"] = dpage
    var err error
    if err != nil {
        funcName, file, line, ok := runtime.Caller(0)
        if ok {
            log.Println("Func Name=" + runtime.FuncForPC(funcName).Name())
            log.Println("file: %s    line=%d", file, line)
            log.Println("%s %s %s", c.Request.RemoteAddr, c.Request.Method, c.Request.URL)
        }
    }
    log.Println("begin editsave")
    return c.Redirect("/")
}

func (c CONTROLLERNAME)  Delete(my_id string) revel.Result {
    if !c.CheckIsEditorLogin() {
        log.Println("user is not editor , so redirect.")
        return c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin delete")
    return c.Redirect("/")
}
func (c CONTROLLERNAME)  Remove(my_id string) revel.Result {
    if !c.CheckIsEditorLogin() {
        log.Println("user is not editor , so redirect.")
        return c.Redirect("/")
    }
    dpage := c.GetMBody()
    dpage.MBody["my_id"] = my_id
    c.RenderArgs["dpage"] = dpage
    log.Println("begin remove")
    return c.Redirect("/")
}
*/
    """
    dir_str = ""
    is_find, dir_list = godroid_helper.get_package_dir_list_from_package_name(profile_instance, model_domain)
    if is_find:
        for one in dir_list:
            dir_str = dir_str + one +"/" 
        dir_str = dir_str[:-1]
        tmplt = tmplt.replace("HTMLPACKAGEDIRNAME", dir_str)
        pass
    else:
        tmplt = tmplt.replace("HTMLPACKAGEDIRNAME", profile_instance.PackageName)
        pass
    tmplt = tmplt.replace("CONTROLLERNAME", profile_instance.ControlCalssName)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)


    #for save new 
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
    condi_fields_user_input = condi_fields_user_input.replace(" user_id","")
    condi_fields_user_input = condi_fields_user_input.replace("read_status","")
    tmplt = tmplt.replace("CONDIFIELDS_USER_INPUT" , condi_fields_user_input )


    #
    return tmplt





def __self_call_get_package( contents_list ):
    return sub_gene_comm.get_go_file_header(contents_list)

def __self_call_get_custom_part(contents_list):
    content = ""
    content = content + sub_gene_comm.GoTemplateCustomPartBegin + "\n"
    content = content + sub_gene_comm.get_go_file_custom_part( contents_list )
    content = content + sub_gene_comm.GoTemplateCustomPartEnd + "\n"
    return content



def __check_controller_meta_flag(file_path):
    comm_funcs.print_ok("......begin __check_controller_meta_flag:" + file_path)
    sub_gene_comm.check_is_go_file_have_meta_flag(file_path)
    return True
    pass


def generate_controller_admin_file(profile_instance, model_domain):
    comm_funcs.print_ok("begin save to controllers admin")
    
    FullPathControllerAdminFile = godroid_helper.get_controller_admin_file_name_full_path(profile_instance, model_domain)
    contents_list = comm_funcs.get_file_content_as_list( FullPathControllerAdminFile )
    part_one = __self_call_get_package(contents_list)
    comm_funcs.print_ok( "controller admin part one:" + part_one )
    #---- begin
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin

    part_package_import = __self_call_get_admin_packages_part(profile_instance, model_domain)

    part_curd = __self_call_get_admin_CURD_part(profile_instance, model_domain)

    part_auto_empty_test_admin = __self_call_get_admin_auto_empty_test_part(profile_instance, model_domain)
    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #---- end

    part_auto_full = part_begin + "\n" + part_package_import + "\n" + part_curd + "\n" + part_auto_empty_test_admin + "\n"+ part_end

    part_custom  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_auto_full + "\n" + part_custom
    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathControllerAdminFile )
    comm_funcs.add_to_exist_file( FullPathControllerAdminFile  , all_file_conent  )    



def print_route_info(profile_instance, model_domain):
    tmplt = """
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### xxxxx brand
GET     /xxxxx/guanli/xxxxxxx/index.html                     CONTROLLERNAME.GuanliIndex
GET     /xxxxx/guanli/xxxxxxx/list.html                      CONTROLLERNAME.GuanliList
GET     /xxxxx/guanli/xxxxxxx/add.html                       CONTROLLERNAME.GuanliAdd
POST    /xxxxx/guanli/xxxxxxx/add_save.html                  CONTROLLERNAME.GuanliAddSave
GET     /xxxxx/guanli/xxxxxxx/edit.html                      CONTROLLERNAME.GuanliEdit
POST    /xxxxx/guanli/xxxxxxx/edit_save.html                 CONTROLLERNAME.GuanliEditSave
GET     /xxxxx/guanli/xxxxxxx/delete.html                    CONTROLLERNAME.GuanliDelete
GET     /xxxxx/guanli/xxxxxxx/remove.html                    CONTROLLERNAME.GuanliRemove
### --- --- --- --- --- --- --- --- --- --- --- --- ---
GET     /xxxxx/guanli/xxxxxxx/index.html                     CONTROLLERNAME.Index
GET     /xxxxx/guanli/xxxxxxx/list.html                      CONTROLLERNAME.List
#GET     /xxxxx/guanli/xxxxxxx/add.html                       CONTROLLERNAME.Add
#POST    /xxxxx/guanli/xxxxxxx/add_save.html                  CONTROLLERNAME.AddSave
#GET     /xxxxx/guanli/xxxxxxx/edit.html                      CONTROLLERNAME.Edit
#POST    /xxxxx/guanli/xxxxxxx/edit_save.html                 CONTROLLERNAME.EditSave
#GET     /xxxxx/guanli/xxxxxxx/delete.html                    CONTROLLERNAME.Delete
#GET     /xxxxx/guanli/xxxxxxx/remove.html                    CONTROLLERNAME.Remove
### --- --- --- --- --- --- --- --- --- --- --- --- ---
POST    /api/v1/car/xxxxxxx/add.html                       CONTROLLERNAME.ApiV1Add

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    """
    tmplt = tmplt.replace("CONTROLLERNAME", profile_instance.ControlCalssName)
    return tmplt


def generate_controller_file(profile_instance, model_domain):
    generate_controller_show_file(profile_instance, model_domain)
    generate_controller_admin_file(profile_instance, model_domain)
    print print_route_info(profile_instance, model_domain)
    pass

def generate_controller_show_file(profile_instance, model_domain):
    comm_funcs.print_ok("begin save to controllers")


    FullPathControllerFile = godroid_helper.get_controller_file_name_full_path(profile_instance, model_domain)

    contents_list = comm_funcs.get_file_content_as_list( FullPathControllerFile )

    part_one = __self_call_get_package(contents_list)
    comm_funcs.print_ok( "controller part one:" + part_one )
    #---- begin
    part_begin = sub_gene_comm.GoTemplateAutoPartBegin

    part_package_import = __self_call_get_packages_part(profile_instance, model_domain)

    part_curd = __self_call_get_CURD_part(profile_instance, model_domain)

    part_auto_empty_test = __self_call_get_auto_empty_test_part(profile_instance, model_domain)

    part_end = sub_gene_comm.GoTemplateAutoPartEnd
    #---- end

    part_auto_full = part_begin + "\n" + part_package_import + "\n" + part_curd +"\n" + part_auto_empty_test + "\n"+ part_end

    part_custom  = __self_call_get_custom_part(contents_list)
    all_file_conent = part_one + "\n" + part_auto_full + "\n" + part_custom
    sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( FullPathControllerFile )
    comm_funcs.add_to_exist_file( FullPathControllerFile  , all_file_conent  )




    pass
