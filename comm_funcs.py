# -*- coding: utf-8 –*-
import sys
reload(sys)
import os
import fnmatch
sys.path.append(os.getcwd())
sys.setdefaultencoding('utf8')


### ### ### ### ### ### ### ### ### ### ### ### 
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def print_color(text, colour=WHITE):
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)

def print_ok( text  ):
    print_color(text + "\n", GREEN)
def print_error(text):
    print_color(text + "\n", RED)

    
def helloworld():
    print "helloworld"

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]








    pass

def walk_dir_rename_dir_to_lowercase(some_path):
    print_ok("begin walk path:" + some_path )
    for root, dirs, files in os.walk(some_path):
        for one_dir in dirs:
            ori_dir = one_dir
            lower_dir = ori_dir.lower()
            if ori_dir in lower_dir:
                print_ok( "------" )
                continue
            print_error( one_dir )
            ori_dir_full = os.path.join(root, ori_dir) 
            lower_dir_full = os.path.join(root, lower_dir) 
            cmd_mv = " mv  " + ori_dir_full + " " + lower_dir_full
            print_ok( cmd_mv )
            #os.system( cmd_mv )

    pass

def walk_dir_rename__just_file_to_lowercase_tmp_code(some_path,pattern = '*.html'):
    print_ok("begin walk path:" + some_path )
    for root, dirs, files in os.walk(some_path):
        for filename in fnmatch.filter(files, pattern):
            if filename.startswith("."):
                print_error("invalid:" + one_filename )
                continue
            ori_fn = filename
            lower_fn = ori_fn.lower()
            if ori_fn in lower_fn:
                continue
            new_filename_full = os.path.join(root, lower_fn)
            ori_filename_full = os.path.join(root, filename)
            mv_cmd = "mv " + ori_filename_full + " " + new_filename_full
            #print_ok( ori_filename_full )
            print_ok( mv_cmd )
            #os.system( mv_cmd )

    return
    for directory, dirnames, filenames in os.walk(some_path):
        for one_dir in dirnames:        
            for one_filename in filenames:
                if one_filename.startswith("."):
                    print_error("invalid:" + one_filename )
                    continue
                print_ok(join(directory, name) for name in filenames)
                continue
                ori_filename_full = directory + "/" + one_dir +"/" + one_filename
                ori_fn = one_filename
                lower_fn = ori_fn.lower()
                new_filename_full = directory + "/" + one_dir +"/" + lower_fn
                if ori_fn in lower_fn:
                    continue
                    #print_ok( directory + "/" + one_dir +"/" + one_filename )
                else:
                    print_error( ori_filename_full  )
                    mv_cmd = "mv " + ori_filename_full + " " + new_filename_full
                    print_ok( mv_cmd )
                    #os.system( mv_cmd )



def remove_all_html_files_in_dir(dir_name):
    os.system( "rm -f " + dir_name + " *.html " )

def add_to_exist_file( file_name , line ):
    with open( file_name , "r+U") as f:
        try:
            f.seek(-1, 2)
            while f.read(1) == "\n":
                f.seek(-2, 1)      # go back two characters, since
                # reading advances by one character
        except IOError:            # seek failed, so the file consists
            f.seek(0)              # exclusively of newline characters
        #else:
        #    f.write("\n")          # Add exactly one newline character
        if not line.endswith("\n"):
            line = line + "\n"
        f.write( line )        # Add a new line


def get_file_content_as_list( file_name ):
    f = open( file_name )
    lines = f.readlines()
    f.close()
    return lines

def get_gopath():
    return os.environ['GOPATH']

def check_and_get_go_path():
    gopath = get_gopath()
    if gopath is None or 0 == len(gopath):
        print_error("ERROR: evn go path not set ")
        sys.exit(1)
    return gopath 


def get_projects_str():
    gopath = get_gopath()
    if 0 == len(gopath):
        print_error( "ERROR GOPATH not set." )
        sys.exit(1)
    proj_file = gopath + "/gobbs_projects.txt"
    if not os.path.exists( proj_file ):
        print_error("ERROR proj_file not exit :" + proj_file )
        sys.exit(1)
    contents = get_file_content_as_list(proj_file)
    cs = ""
    for one in contents:
        cs = cs + " " + one
    return cs

def check_app_type_and_instance_name( app_type , instance_name ):
    print "app type:", app_type
    if app_type not in get_projects_str():
        print_error("ERROR\n")
        print_error(  "not find app type:"+ app_type )
        return False
    print "instance name:", instance_name
    # how to check instance name?
    mydir = os.getcwd()
    src_dir = mydir + "/src"
    app_dir = src_dir + "/" + app_type
    app_views_dir = src_dir + "/" + app_type +"_views"
    files = listdir_fullpath( app_views_dir )
    all_instance_name = ""
    find_instance = False
    for one in files:
        if not os.path.isdir( one ):
            continue
        one = one.replace( app_views_dir , "" )[1:]
        if one == instance_name:
            find_instance = True
        all_instance_name = all_instance_name + " " + one 
    if not find_instance :
            print_error( "instance :" + instance_name + " not in instance_name list :"  )
            print all_instance_name
            return False
    return True

def touch(fname, times=None):
    """
    touch - change file timestamps
    """
    with file(fname, 'wa'):
        os.utime(fname, times)

def backup_and_write_new_file():
    pass


if __name__ == "__main__":
    print os.environ['HOME']
    #print os.environ['GOPATH']
    #/gobbs/app/views/default/
    gopath = "/programming/go/gohome/src/gobbs_views/"
    walk_dir_rename_dir_to_lowercase( gopath )
    #walk_dir_rename__just_file_to_lowercase_tmp_code( gopath + "/" + "src/gobbs/app/views" )


    


