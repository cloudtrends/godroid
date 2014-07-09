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
    comm_funcs.print_ok("   htmlcurd  :" + line )
def print_error(line):
    comm_funcs.print_error("   htmlcurd  :" + line )


def ______comm_begin_part():
    tmplt = """

{{ $my_id           := .dpage.MBody.my_id          }}
{{ $action         := .dpage.MBody.action         }}
{{ $query_values   := .dpage.QueryValues          }}
{{ $form_values    := .dpage.FormValues           }}
{{set . "title"         .dpage.Title              }}
{{set . "description"   .dpage.Desc               }}
{{set . "keywords"      .dpage.Keywords           }}
{{template "default/header.html"                 .}}
{{template "default/main_menu.html"              .}}

<div id="wrap"><div class="container" id="page-main"><div class="row">
<div class="span10"><div class="box">

    """
    return tmplt

def ____comm_end_part():
    tmplt = """

</div></div>
</div></div></div>

{{template "default/footer.html"                   .}}

    """

    return tmplt




def __self_call_generate_file_new(profile_instance, model_domain):
    tmplt = """

    <div class="box-header">
    新增
    </div>
    <div class="cell topic">
    {{ $one_item := GetEmptyCLASSNAME }}
    {{ set . "one_item"   $one_item }}
    {{template "xxxxx/xxxxx/FUNCTIONNAME/xxxxx/m_new.html"               . }}
    </div>

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_save_new(profile_instance, model_domain):
    tmplt = """


    <div class="box-header">
    
    </div>
    <div class="cell topic">
{{ $filled_obj := FillNewCLASSNAME  $form_values }}
{{ $my_id := GetUniqueId }}
{{ $filled_obj := UpdateFieldCLASSNAME $filled_obj "MyId"  $my_id }}
{{ $filled_obj := UpdateFieldCLASSNAME $filled_obj "ReadStatus"  1 }}

{{ $curd := SaveNewCLASSNAME $filled_obj }}
{{if eq $curd.IsOk  true }}
    成功保存
    <a href="/admins/FUNCTIONNAME/main/list/all">返回列表</a>
{{else}}
    保存失败。{{ $curd.Error }}
{{end}}
</div>

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_m_new(profile_instance, model_domain):
    tmplt_input = """
<tr >
<td>SHOWNAME</td><td><input type="text" length="80" size="30" name="SQLNAME" value="{{ .one_item.GONAME }}"></td>
</tr>

    """

    tmplt_input_all = ""
    for one in sub_gene_comm.get_all_sql_fileds_as_list(profile_instance):
        tmp_str = tmplt_input.replace( "SQLNAME" , one )
        tmp_str = tmp_str.replace("GONAME", sub_gene_comm.get_one_go_name_by_sql_name(profile_instance,  one))
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_sql_name(profile_instance,  one))

        tmplt_input_all = tmplt_input_all + tmp_str


    tmplt = """

    <div class="box-header">
    
    </div>
    <div class="cell topic">

<table class="table">
{{ if eq .edit_mode  true }}
<form method="post" action="/admins/FUNCTIONNAME/main/save_edit/{{ .one_item.MyId }}">
<input type="hidden" name="my_id" value="{{ .one_item.MyId }}">

{{else}}
<form method="post" action="/admins/FUNCTIONNAME/main/save_new/new">
{{end}}
<input type="hidden" name="" value="" >

INPUTALLFIELDS

<!-- -->
<input type="submit"  id="btn_submit" name="btn_submit"  value="提交" >
</form>

</table>


</div>

    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = tmplt.replace("INPUTALLFIELDS" , tmplt_input_all)
    tmplt =   tmplt  
    return tmplt

def __self_call_generate_file_edit(profile_instance, model_domain):
    tmplt = """


    <div class="box-header">
    编辑
    </div>

    <div class="cell topic">
    {{ $one_item := GetOneCLASSNAME $my_id  }}
    {{ set . "one_item"   $one_item }}
    {{ set . "edit_mode"  true }}
    {{template "default/admins/FUNCTIONNAME/m_new.html"               . }}
    </div>


    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt


def __self_call_generate_file_save_edit(profile_instance, model_domain):
    update_all_str = ""
    for one in sub_gene_comm.get_all_sql_fileds_as_list(profile_instance):
        update_all_str = update_all_str + "\n" + "{{ $edit_obj := UpdateFieldCLASSNAME $edit_obj \"GONAME\" $filled_obj.GONAME }}"
        update_all_str = update_all_str.replace("GONAME",  sub_gene_comm.get_one_go_name_by_sql_name(profile_instance,  one))
        update_all_str = update_all_str.replace("CLASSNAME",  profile_instance.ClassName )

    tmplt = """

{{ $edit_obj      := GetOneCLASSNAME     $my_id                           }}
{{ $filled_obj    := FillNewCLASSNAME    $form_values                     }}


UPDATEALLSTR

{{ $curd := SaveEditCLASSNAME $edit_obj }}
{{if eq $curd.IsOk  true }}
    成功保存
    <a href="/admins/FUNCTIONNAME/main/list/all">返回列表</a>
{{else}}
    保存失败。{{ $curd.Error }}
{{end}}


    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = tmplt.replace("UPDATEALLSTR" , update_all_str)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_show(profile_instance, model_domain):
    tmplt = """



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt


def __self_call_generate_file_m_show(profile_instance, model_domain):
    tmplt_show = """
<td>
    {{ .one_item.GONAME }}
</td>

    """
    tmplt_show_all = ""
    for one in sub_gene_comm.get_all_golang_fileds_as_list(profile_instance):
        tmp_str = tmplt_show.replace( "GONAME" , one  )
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_go_name(profile_instance,  one))
        tmplt_show_all = tmplt_show_all + tmp_str

    

    tmplt = """
<table class="table">
<tr>
    SHOWALLFIELDS
</tr></table>
    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = tmplt.replace("SHOWALLFIELDS" , tmplt_show_all)
    tmplt =   tmplt  
    return tmplt


def __self_call_generate_file_delete(profile_instance, model_domain):
    tmplt = """


    <div class="box-header">
    成功删除
    </div>
    <div class="cell topic">
{{ $status := DeleteCLASSNAMEByMyId $my_id }}

<a href="/admins/FUNCTIONNAME/main/list/all">返回列表</a>
    </div>
    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_save_delete(profile_instance, model_domain):
    tmplt = """



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt


def __self_call_generate_file_remove(profile_instance, model_domain):
    tmplt = """

    <div class="box-header">
    成功物理删除
    </div>
    <div class="cell topic">
{{ $status := RemoveCLASSNAMEByMyId $my_id }}

<a href="/admins/FUNCTIONNAME/main/list/all">返回列表</a>
    </div>
    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_save_remove(profile_instance, model_domain):
    tmplt = """



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_list(profile_instance, model_domain):
    tmplt_show = """
<td>
    {{ .one_item.GONAME }}
</td>

    """
    tmplt_show_all = ""
    for one in sub_gene_comm.get_all_golang_fileds_as_list(profile_instance):
        tmp_str = tmplt_show.replace( "GONAME" , one  )
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_go_name(profile_instance,  one))
        tmplt_show_all = tmplt_show_all + tmp_str




    tmplt = """



    <div class="box-header">
    <a href="/admins/FUNCTIONNAME/main/new/new">新增</a>
    </div>
    <div class="cell topic">
    {{ $items := GetAllCLASSNAME  1000 0 }}
    {{ set . "items" $items }}
    {{template "default/admins/FUNCTIONNAME/xxx/m_list.html"               . }}
    </div>



{{ $uuid           := .dpage.MBody.uuid           }}
{{ $browser        := GetBrowserInfo    $uuid     }}
<div class="alert">
    {{if eq $browser.IsBrowser  true}}
        {{if eq $browser.BrowserType  1}}IE{{end}}
        {{if eq $browser.BrowserType  2}}FireFox{{end}}
        {{if eq $browser.BrowserType  3}}Chrome{{end}}
        {{if eq $browser.BrowserType  4}}Safari{{end}}
    {{end}}
    {{if eq $browser.OS  1}}Windows{{end}}
    {{if eq $browser.OS  2}}Mac{{end}}
    {{if eq $browser.OS  3}}Android{{end}}
    {{if eq $browser.OS  4}}Linux{{end}}
    {{if eq $browser.OS  5}}IPhone{{end}}
</div>



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = tmplt.replace("ALLLISTFIELDS" , tmplt_show_all)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt


def __self_call_generate_file_index(profile_instance, model_domain):
    tmplt = """



    """
    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = ______comm_begin_part() + tmplt + ____comm_end_part()
    return tmplt

def __self_call_generate_file_m_list(profile_instance, model_domain):
    tmplt_show = """
<td>
    {{ $one_item.GONAME }}
</td>

    """
    tmplt_show_all = ""
    for one in sub_gene_comm.get_all_golang_fileds_as_list(profile_instance):
        tmp_str = tmplt_show.replace( "GONAME" , one  )
        tmp_str = tmp_str.replace("SHOWNAME", sub_gene_comm.get_one_show_name_by_go_name(profile_instance,  one))
        tmplt_show_all = tmplt_show_all + tmp_str

    

    tmplt = """



<table class="table">
{{ range $one_item := .items }}
    <tr >
    <td ><a href="/admins/FUNCTIONNAME/main/edit/{{ $one_item.MyId }}">编辑</a></td>
    <td ><a href="/admins/FUNCTIONNAME/main/delete/{{ $one_item.MyId }}">删除</a></td>
    ALLLISTFIELDS
    <td ><a href="/admins/FUNCTIONNAME/main/remove/{{ $one_item.MyId }}">物理删除</a></td>
    </tr>
{{ end }}
</table>



    """

    tmplt = tmplt.replace("PACKAGENAME", profile_instance.PackageName)
    tmplt = tmplt.replace("MODELDOMAIN", model_domain)
    tmplt = tmplt.replace("CLASSNAME", profile_instance.ClassName)
    tmplt = tmplt.replace("FUNCTIONNAME", profile_instance.FuncName)
    tmplt = tmplt.replace("ALLLISTFIELDS" , tmplt_show_all)
    tmplt =   tmplt  
    return tmplt




def generate_htmlcurl_show_file(profile_instance, model_domain):

    FullPathApiWebModuleNOFILEJUSTDIR = godroid_helper.get_htmlfunc_instance_full_path(profile_instance, model_domain)
    
    if not os.path.exists( FullPathApiWebModuleNOFILEJUSTDIR ):
        comm_funcs.print_ok("api_web_module TIPS:")
        comm_funcs.print_ok("......create for :" + FullPathApiWebModuleNOFILEJUSTDIR )
        os.makedirs(FullPathApiWebModuleNOFILEJUSTDIR)
    else:
        if len( FullPathApiWebModuleNOFILEJUSTDIR ) > 0:
            print_error(" remove all html file in dir :" + FullPathApiWebModuleNOFILEJUSTDIR + "/*.html")
            comm_funcs.remove_all_html_files_in_dir( FullPathApiWebModuleNOFILEJUSTDIR +"/*.html ")


    print_ok(" generate new ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/new.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_new(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate save new ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/save_new.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_save_new(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate m_new ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/m_new.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_m_new(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate edit ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/edit.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_edit(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate save edit ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/save_edit.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_save_edit(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate show ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/show.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_show(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate m_show ")  
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/m_show.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_m_show(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate delete ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/delete.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_delete(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    #print_ok(" generate save delete ")
    #tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/save_delete.html"
    #sub_gene_comm.touch_new_file( tmp_comm_file )
    #content = __self_call_generate_file_save_delete(profile_instance, model_domain)
    #comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate remove ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/remove.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_remove(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    #print_ok(" generate save remove ")
    #tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/save_remove.html"
    #sub_gene_comm.touch_new_file( tmp_comm_file )
    #content = __self_call_generate_file_save_remove(profile_instance, model_domain)
    #comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate list ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/list.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_list(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate index ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/index.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_index(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    print_ok(" generate m_list ")
    tmp_comm_file = FullPathApiWebModuleNOFILEJUSTDIR + "/m_list.html"
    sub_gene_comm.touch_new_file( tmp_comm_file )
    content = __self_call_generate_file_m_list(profile_instance, model_domain)
    comm_funcs.add_to_exist_file( tmp_comm_file  , content  )
    pass


def generate_htmlcurl_file(profile_instance, model_domain):
    """
    htmlcurl
    """

    print_ok("begin generate htmlcurl file ... ")
    generate_htmlcurl_show_file(profile_instance, model_domain)
    pass

