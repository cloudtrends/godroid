# -*- coding: utf-8 –*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
sys.path.append(os.getcwd())
import subprocess
import shutil
import comm_funcs


import sub_gene_class, sub_gene_funcs_gorp, sub_gene_api, sub_gene_comm, sub_gene_controller, sub_gene_api_web_module, sub_gene_revel_curd

def print_ok(line):
    comm_funcs.print_ok("   godroid_helper  :" + line )
def print_error(line):
    comm_funcs.print_error("   godroid_helper  :" + line )




def get_package_dir_list_from_package_name(profile_instance, model_domain):
    """
    convert  gobbs_aaa_bbb  to ['aaa', 'bbb'] or
             jog_xxxx   to ['jog', 'xxxx']
    """
    pkn = profile_instance.PackageName
    if 0 == len(pkn):
        return False, []
    pkns = pkn.split("_")
    results = []
    for one in pkns:
        if one == "gobbs":
            continue
        if profile_instance.IsModule and one == profile_instance.ModuleName:
            continue
        results.append(one)
    #comm_funcs.print_error("TIPS common:" + pkn)
    #print results
    return True, results
    


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
    print_ok("begin get instance from profile:" + profile_path)
    tmp_cls = sub_gene_comm.ClassProfileCfg()
    tmp_cls.ProfileFile = profile_path
    contents_list = comm_funcs.get_file_content_as_list(profile_path)
    for line in contents_list:
        line = line.strip()
        if 0 == len(line):
            continue
        if line.startswith("#"):
            continue
        if "#" in line:
            line = line[: line.find("#") ]
        line = line.strip()
        if 0 == len(line):
            continue
        #
        #GeneCompontents
        if line.startswith("gene_compontents"):
            line = line.replace("gene_compontents=", "")
            tmp_cls.GeneCompontents = line.strip()
            continue
        if line.startswith("is_module"):
            line = line.replace("is_module=", "")
            if "true" in line:
                tmp_cls.IsModule = True
            else:
                tmp_cls.IsModule = False
            pass
        if line.startswith("module_type"):
            line = line.replace("module_type=", "")
            tmp_cls.ModuleType = line.strip()
            if tmp_cls.IsModule and 0 == len(tmp_cls.ModuleType):
                comm_funcs.print_error("Error when parser module type: no  ModuleType ")
                sys.exit(1)
            pass
        if line.startswith("module_name"):
            line = line.replace("module_name=", "")
            tmp_cls.ModuleName = line.strip()
            if tmp_cls.IsModule and 0 == len(tmp_cls.ModuleName):
                comm_funcs.print_error("Error when parser module name: no module name ")
                sys.exit(1)
            pass
        if line.startswith("controller_class_name"):
            line = line.replace("controller_class_name=", "")
            tmp_cls.ControlCalssName = line.strip()
            pass
        if line.startswith("table_name=") :
            line = line.replace("table_name=", "")
            tmp_cls.TableName = line.strip()
        if line.startswith("package_name="):
            line = line.replace("package_name=", "")
            tmp_cls.PackageName = line.strip()
            if 0 == len( tmp_cls.PackageName ):
                print_error("Error package name can not be empty.")
                sys.exit(1)
        if line.startswith("func_name="):
            '''
            func name is just a help field for generate the go file name
            so ,can be empty
            '''
            line = line.replace("func_name=", "")
            tmp_cls.FuncName = line.strip()
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
            if obj.SqlName == "mysql_name" :
                print_error("Error mysql_name should not exist in config file.")
                sys.exit(1)
            obj.SqlType = sql_parts[1]
            obj.GoName = go_parts[0]
            obj.GoType = go_parts[1]
            if 3 <= len(lines):
                part3 = lines[2]
                parts3 = part3.split(",")
                if 2 == len(parts3):
                    if "ShowName" in parts3[0]:
                        obj.ShowName = parts3[1].strip()
                        if obj.ShowName == "XXXXXX":
                            obj.ShowName = obj.GoName
            tmp_cls.ColumnsList.append(obj)
    
    return tmp_cls







### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


def get_domain_model_path(profile_instance,model_domain):
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/model"
    else:
        return gopath + "/src/" + model_domain + "/model"
def get_domain_api_path(profile_instance,model_domain):
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/api"
    else:
        return gopath + "/src/" + model_domain + "/api"


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 



def get_domain_non_module_controller_path(profile_instance, model_domain):
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/gobbs/app/controllers" 
    else:
        return gopath + "/src/gobbs/app/controllers" 
    #return gopath + "/src/gobbs/app/controllers/" +  profile_instance.PackageName

def get_domain_module_controller_path(profile_instance, model_domain):
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/" + profile_instance.ModuleType + "/"+ profile_instance.ModuleName +"/app/controllers" #+  profile_instance.PackageName
    else:
        return gopath + "/src/" + model_domain + "/" + profile_instance.ModuleType + "/"+ profile_instance.ModuleName +"/app/controllers" #+  profile_instance.PackageName


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 


def get_module_revelcurdfuncs_path(profile_instance, model_domain):
    """
    revelcurdfuncs

    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/" + profile_instance.ModuleType + "/"+ profile_instance.ModuleName +"/app/controllers/curdfuncs"  
    else:
        return gopath + "/src/" + model_domain + "/" + profile_instance.ModuleType + "/"+ profile_instance.ModuleName +"/app/controllers/curdfuncs" 
    pass


def get_non_module_revelcurdfuncs_path(profile_instance, model_domain):
    """
    revelcurdfuncs

    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/gobbs/app/controllers/curdfuncs"  
    else:
        return gopath + "/src/gobbs/app/controllers/curdfuncs" 
    pass


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 



def get_non_module_htmlfunc_path(profile_instance, model_domain):
    """
    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/html/" +  profile_instance.PackageName
    else:
        return gopath + "/src/tmp_auto_code/html/" +  profile_instance.PackageName
    pass



def get_module_htmlfunc_path(profile_instance, model_domain):
    """
    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/html/" + profile_instance.ModuleType + "/" + profile_instance.ModuleName
    else:
        return gopath + "/src/tmp_auto_code/html/" + profile_instance.ModuleType + "/" + profile_instance.ModuleName
    pass


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def get_non_module_api_web_module_path(profile_instance,model_domain):
    """
    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/api/web/gobbs" 
    else:
        return gopath + "/src/" + model_domain + "/api/web/gobbs"  
    pass

def get_module_api_web_module_path(profile_instance, model_domain):
    """
    """
    gopath = comm_funcs.get_gopath()
    if profile_instance.IsDevMode:
        return gopath + "/src/tmp_auto_code/" + model_domain + "/api/" + profile_instance.ModuleType + "/" + profile_instance.ModuleName
    else:
        return gopath + "/src/" + model_domain + "/api/" + profile_instance.ModuleType + "/" + profile_instance.ModuleName
    pass

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def get_revel_curd_funcs_instance_full_path(profile_instance, model_domain):
    """
    revelcurdfuncs
    """
    if profile_instance.IsModule:
        return get_module_revelcurdfuncs_path(profile_instance, model_domain)
    else:
        return get_non_module_revelcurdfuncs_path(profile_instance, model_domain) 
    pass


def get_htmlfunc_instance_full_path(profile_instance, model_domain):
    """
    """
    if profile_instance.IsModule:
        return get_module_htmlfunc_path(profile_instance, model_domain)
    else:
        return get_non_module_htmlfunc_path(profile_instance, model_domain) 
    pass

def get_api_web_module_instance_full_path(profile_instance, model_domain):
    """

    """
    if profile_instance.IsModule:
        return get_module_api_web_module_path(profile_instance, model_domain)
    else:
        return get_non_module_api_web_module_path(profile_instance, model_domain)
    pass

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 



def get_domain_controller_instance_full_path(profile_instance, model_domain):
    """
    1. is module ?
        module path 
        such as :  ${gopath}/src/{model_domain}/{module_type}/app/controllers
    2. not module 
        not module path 
        such as : ${gopath}/src/gobbs/app/controllers/{self_package_name}
    """
    if profile_instance.IsModule:
        return get_domain_module_controller_path(profile_instance, model_domain)
    else:
        return get_domain_non_module_controller_path(profile_instance, model_domain)
        pass
    comm_funcs.print_error("Error when get get_domain_controller_instance_full_path")
    sys.exit(1)
    return None
    pass

def get_domain_model_instance_full_path(profile_instance, model_domain):
    if profile_instance.IsModule:
        return get_domain_model_path(profile_instance,model_domain) + "/" + profile_instance.ModuleType + "/" +  profile_instance.ModuleName  + "/" + profile_instance.PackageName  
    else:
        return get_domain_model_path(profile_instance,model_domain) + "/" + profile_instance.PackageName 
    pass
def get_domain_api_instance_full_path(profile_instance, model_domain):
    '''
    20140327
    api/web[module_type]
            module_name[module_name]
                                [package_name]
            package_name

    '''
    if profile_instance.IsModule:
        return get_domain_api_path(profile_instance,model_domain) + "/" + profile_instance.ModuleType + "/" +  profile_instance.ModuleName  + "/" + profile_instance.PackageName  
    else:
        return get_domain_api_path(profile_instance,model_domain) + "/" + profile_instance.PackageName  
    pass

#---------------


def get_revelcurdfuncs_file_name(profile_instance):
    revelcurdfuncs_file_name = "curd_funcs_" + profile_instance.PackageName + "_" + profile_instance.FuncName + profile_instance.FileExt
    return revelcurdfuncs_file_name

def get_apiwebmodule_file_name(profile_instance):
    apiwebmodule_file_name = "cds_" + profile_instance.PackageName + "_" + profile_instance.FuncName + profile_instance.FileExt
    return apiwebmodule_file_name

def get_controller_admin_file_name(profile_instance):
    controller_file_name = profile_instance.PackageName + "_admin" + profile_instance.FileExt
    return controller_file_name
def get_controller_file_name(profile_instance):
    controller_file_name = profile_instance.PackageName + profile_instance.FileExt
    return controller_file_name
def get_model_class_file_name(profile_instance):
    model_file_name = "m_" + profile_instance.PackageName + profile_instance.FileExt
    return model_file_name
def get_model_funcs_of_gorp_file_name(profile_instance):
    funcs_of_gorp_file_name = "gorp_"+ profile_instance.PackageName  + profile_instance.FileExt
    return funcs_of_gorp_file_name
def get_api_file_name(profile_instance):
    api_file_name = "api_" + profile_instance.PackageName + profile_instance.FileExt
    return api_file_name

#---------------

def get_controller_admin_file_name_full_path(profile_instance, model_domain):
    return get_domain_controller_instance_full_path(profile_instance, model_domain) + "/" + get_controller_admin_file_name(profile_instance)


def get_revelcurdfuncs_file_name_full_path(profile_instance, model_domain):
    """
    revelcurdfuncs
    """
    return get_revel_curd_funcs_instance_full_path(profile_instance, model_domain) + "/"  + get_revelcurdfuncs_file_name(profile_instance)

def get_apiwebmodule_file_name_full_path(profile_instance, model_domain):
    return get_api_web_module_instance_full_path(profile_instance, model_domain) + "/"  + get_apiwebmodule_file_name(profile_instance)

def get_controller_file_name_full_path(profile_instance, model_domain):
    return get_domain_controller_instance_full_path(profile_instance, model_domain) + "/" + get_controller_file_name(profile_instance)


def get_model_funcs_of_gorp_file_name_full_path(profile_instance, model_domain):
    return get_domain_model_instance_full_path(profile_instance, model_domain) + "/" + get_model_funcs_of_gorp_file_name(profile_instance)
def get_model_class_file_name_full_path(profile_instance, model_domain):
    return get_domain_model_instance_full_path(profile_instance, model_domain) + "/" + get_model_class_file_name(profile_instance)
def get_api_file_name_full_path(profile_instance, model_domain):
    return get_domain_api_instance_full_path(profile_instance, model_domain)+ "/" + get_api_file_name(profile_instance)

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def touch_and_create_apiwebgobbs_file(file_full_path, profile_instance):
    """
    package curdfuncs
    """
    comm_funcs.touch(file_full_path)
    template_lines = sub_gene_comm.GoEmptyFileTemplate
    template_lines = template_lines.replace( "PACKAGENAME", "gobbs" )
    comm_funcs.add_to_exist_file(file_full_path, template_lines)    
    pass



def touch_and_create_revelcurdfuncs_file(file_full_path, profile_instance):
    """
    package curdfuncs
    """
    comm_funcs.touch(file_full_path)
    template_lines = sub_gene_comm.GoEmptyFileTemplate
    template_lines = template_lines.replace( "PACKAGENAME", "curdfuncs" )
    comm_funcs.add_to_exist_file(file_full_path, template_lines)    
    pass




def touch_and_create_empty_controller_file(file_full_path, profile_instance):
    """
    controllers alwayz is controllers
    """
    comm_funcs.touch(file_full_path)
    template_lines = sub_gene_comm.GoEmptyFileTemplate
    template_lines = template_lines.replace( "PACKAGENAME", "controllers" )
    comm_funcs.add_to_exist_file(file_full_path, template_lines)    
    pass



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

def check_revel_curd_funcs_meta_flag(profile_instance, model_domain):
    """
    revel_curd_funcs
    revelcurdfuncs
    """
    revel_curd_funcs_instance_full_path = get_revel_curd_funcs_instance_full_path(profile_instance, model_domain)
    if not os.path.exists( revel_curd_funcs_instance_full_path ):
        comm_funcs.print_ok("api_web_module TIPS:")
        comm_funcs.print_ok("......create for :" + revel_curd_funcs_instance_full_path )
        os.makedirs(revel_curd_funcs_instance_full_path)  
    FullPathRevelCurdFuncsFile = get_revelcurdfuncs_file_name_full_path(profile_instance, model_domain) 
    if not os.path.exists(FullPathRevelCurdFuncsFile):
        touch_and_create_revelcurdfuncs_file(FullPathRevelCurdFuncsFile, profile_instance)
    comm_funcs.print_ok(">>>> begin check revel_curd_funcs meta flag is valid")
    revelcurdfuncs_file_valid = False
    revelcurdfuncs_file_valid = sub_gene_revel_curd.__check_revelcurdfuncs_meta_flag(FullPathRevelCurdFuncsFile)
    return True
    pass

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def check_api_web_module_meta_flag(profile_instance, model_domain):
    """
    api_web_module
    """
    api_web_module_instance_full_path = get_api_web_module_instance_full_path(profile_instance, model_domain)
    if not os.path.exists( api_web_module_instance_full_path ):
        comm_funcs.print_ok("api_web_module TIPS:")
        comm_funcs.print_ok("......create for :" + api_web_module_instance_full_path )
        os.makedirs(api_web_module_instance_full_path)
    FullPathApiWebModuleFile = get_apiwebmodule_file_name_full_path(profile_instance, model_domain)
    if not os.path.exists(FullPathApiWebModuleFile):
        touch_and_create_apiwebgobbs_file(FullPathApiWebModuleFile, profile_instance)
    comm_funcs.print_ok("GodroidHelper>>>> begin check api_web_module meta flag is valid")
    api_web_module_file_valid = False
    api_web_module_file_valid = sub_gene_api_web_module.__check_apiwebmodule_meta_flag(FullPathApiWebModuleFile)
    print_ok("Done")
    return True
    pass




### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 

def check_controller_meta_flag( profile_instance, model_domain ):
    """
    controller have two type :  inline and in module.
    so ...
    """
    comm_funcs.print_ok("begin check controller ")
    domain_controller_instance_full_path = get_domain_controller_instance_full_path(profile_instance, model_domain)
    if not os.path.exists(domain_controller_instance_full_path):
        comm_funcs.print_ok("TIPS")
        comm_funcs.print_ok("...... create for :" + domain_controller_instance_full_path )
        os.makedirs(domain_controller_instance_full_path)
    #comm_funcs.print_error(domain_controller_instance_full_path)

    FullPathControllerFile = get_controller_file_name_full_path(profile_instance, model_domain)

    
    
    #comm_funcs.print_ok(FullPathControllerFile)
    if not os.path.exists(FullPathControllerFile):
        touch_and_create_empty_controller_file(FullPathControllerFile, profile_instance)
    comm_funcs.print_ok(">>>> begin check controller meta flag is valid")
    controller_file_valid = False
    controller_file_valid = sub_gene_controller.__check_controller_meta_flag(FullPathControllerFile)

    # admin file
    FullPathControllerAdminFile = get_controller_admin_file_name_full_path(profile_instance, model_domain)
    if not os.path.exists(FullPathControllerAdminFile):
        touch_and_create_empty_controller_file(FullPathControllerAdminFile, profile_instance)
    controller_file_valid = False
    controller_file_valid = sub_gene_controller.__check_controller_meta_flag(FullPathControllerAdminFile)    
    return True


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
    """
    repelate columns

    
    """
    maps_columns = {}
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
        if first_parts[0] not in maps_columns.keys():
            maps_columns[first_parts[0]] = first_parts[0]
        else:
            error(" cfg file columns DUPLICATED ( X,X;X,X ) :" + first_parts[0] )
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




def walk_dir_add_magic_tag_to_files(some_path, pattern = '*.go'):
    for root, dirs, files in os.walk(some_path):
        for filename in fnmatch.filter(files, pattern):
            if filename.startswith("."):
                print_error("invalid:" + one_filename )
                continue
            #check magic tag
            #if yes , continue
            #else read content then add tag 
            #backup original file and create new file
            file_path =  os.path.join(root, filename)
            if sub_gene_comm.check_is_go_file_have_meta_flag( file_path ):
                continue
            all_file_conent = ""
            contents_list = comm_funcs.get_file_content_as_list( file_path )
            all_original_code = ""
            line_num = 0
            for line in contents_list:
                if 0 == line_num:
                    line_num = line_num + 1
                    continue
                line_num = line_num + 1
                all_original_code = all_original_code + line
            all_file_conent = all_file_conent + contents_list[0] + "\n" 
            # add empty line
            all_file_conent = all_file_conent + "\n" 
            all_file_conent = all_file_conent + GoTemplateMagicSecondLine  + "\n"
            all_file_conent = all_file_conent + GoTemplateAutoPartBegin + "\n"
            all_file_conent = all_file_conent + GoTemplateAutoPartEnd  + "\n" 
            all_file_conent = all_file_conent + GoTemplateCustomPartBegin  + "\n"
            all_file_conent =  all_file_conent + all_original_code
            all_file_conent = all_file_conent + GoTemplateCustomPartEnd  + "\n"
            sub_gene_comm.backup_go_file_in_curr_dir_and_touch_new_one( file_path )
            comm_funcs.add_to_exist_file( file_path  , all_file_conent  )



if "__main__" == __name__:
    some_path = ""
    walk_dir_add_magic_tag_to_files(some_path)
    pass



