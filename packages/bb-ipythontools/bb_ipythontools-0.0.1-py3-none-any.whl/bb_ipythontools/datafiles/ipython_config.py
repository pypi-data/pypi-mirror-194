# Configuration file for ipython. - Modified by BB-iPythonTools

#-----------------------------------------------------------------------------#
#                                                                             #
#   Main configuration file location                                          #
#       "$HOME/.ipython/profile_${PROFILE_NAME}/ipython_config.py"            #
#                                                                             #
#       ADD NEW CONFIGURATIONS BELOW THE '^^^' LINE                           #
#                                                                             #
#   - do not change the order of the top code in this file                    #
#                                                                             #
#-----------------------------------------------------------------------------#
#   Create empty config file if not existing and lockfile is found            #
#       [ default = True ]                                                    #
#-----------------------------------------------------------------------------#

# Set config file to be created if not yet existing [default = True]
create_project_config = True
run_custom_config = True

# Add exec lines globally for iPython
#  - use .iPythonStartup.py in root of project folder for local exec lines
USER_ADDED = []

#-----------------------------------------------------------------------------#
# Load iPython configuration module                                           #
#-----------------------------------------------------------------------------#
c = get_config()  # noqa

#-----------------------------------------------------------------------------#
#   Custom config - BB-iPythonConfig                                          #
#-----------------------------------------------------------------------------#

exec_lines = []
err_lines  = []

# colors
c_G = '\x1b[0;2;37;3m'     # gray      <i>
c_W = '\x1b[0;1;37m'       # white
c_C = '\x1b[0;0;36;3m'     # cyan      <i>
c_P = '\x1b[0;0;35;3m'     # purple    <i>
c_B = '\x1b[0;1;34;3m'     # blue      <i>
c_R = '\x1b[0;1;31m'       # red
c_Y = '\x1b[0;1;33m'       # yellow
__  = '\x1b[0;0;37m'       # light gray
_   = '\x1b[0m'            # RESET

if run_custom_config:
    try:
        from bb_ipythontools import main
    except ImportError:
        x = f"{c_Y}\n  [WARNING]{c_G} Install bb_ipythontools to use custom config file{_}"
        err_lines += [ f"print({repr(x)})" ]
        run_custom_config = False

if run_custom_config:
    from glob import glob
    import re, sys
    from os import getcwd
    from os.path import join, isfile, expanduser, dirname, basename

    # Variables
    HOME = expanduser('~')
    PWD   = getcwd()

    def ERR(msg = ""):
        R = f"\n\x1b[1;31m  [ERROR]{c_G}  {msg}{_}"
        return R

    def WARN(msg = ""):
        R = f"\n\x1b[1;33m  [WARNING]{c_G}  {msg}{_}"
        return R

    #-----------------------------------------------------------------------------#
    #   Find root project folder if existing                                      #
    #-----------------------------------------------------------------------------#

    conf = main()
    project_directory, project_config_file = conf.findlockDir()

    #-----------------------------------------------------------------------------#
    #   Load default config lines                                                 #
    #-----------------------------------------------------------------------------#

    muh_startup_info = '\n      '.join([ f'\n        {c_W}>>>  {__}'.join([ f"\n{c_W}    Modules Loaded{c_G} from{c_C} ipython_config.py{__}\n",
                                                                            f"{c_B}import{__} sys, os, tempfile, functools, logging",
                                                                            f"{c_P}from{__} os{c_B} import{c_W} ({__} devnull,",
                                                                            f"                 pathsep,",
                                                                            f"                 getcwd{c_B} as{c_W} PWD{__},",
                                                                            f"                 listdir{c_B} as{c_W} LS )",
                                                                            f"{c_P}from{__} os.path{c_B} import{c_W} ({__} expanduser,",
                                                                            f"                      isdir,",
                                                                            f"                      isfile,",
                                                                            f"                      splitext,",
                                                                            f"                      basename{c_B} as{c_W} BN{__},",
                                                                            f"                      dirname{c_B} as{c_W} DN{__},",
                                                                            f"                      join{c_B} as{c_W} JN ){_}\n" ]),
                                         f"{c_W}Partial Function:{__} HOME ={c_B} functools{__}.{c_B}partial{c_W}({c_G} expanduser{__},{c_G} '~'{c_W} ){_}\n" ])

    exec_lines += [ "import sys, os, tempfile, functools, logging",
                    "from os import ( listdir as LS, getcwd as PWD, devnull, pathsep )",
                    "from os.path import ( join as JN, basename as BN, dirname as DN, expanduser, isdir, isfile, splitext )",
                    "HOME = functools.partial( expanduser, '~' )",
                    f"def getIpythonStartupLines() : print({repr(muh_startup_info)})",
                    "getIpythonStartupLines()" ]

    x = [ f"{c_W}      *{c_G} You can show the above message anytime with{__} getIpythonStartupLines(){_}" ]
    if not project_directory:
        x += [ f"\x1b[1;33m\n          [WARNING]{c_G}  Project root directory was not determined{_}" ]

    x2 = '\n'.join(x)
    exec_lines += [ f"print({repr(x2)})" ]

    #-----------------------------------------------------------------------------#
    #   Load project config                                                       #
    #-----------------------------------------------------------------------------#

    if isfile(project_config_file):
        try:
            pcfTxt = []
            cf = conf.getLines('lines')
            if not cf:
                raise ValueError
            exec_lines += cf
            pcfTxt += [ f"{c_W}    Successfully added{c_C} {project_config_file}{c_W} to configuration{_}",
                        f"{c_W}      -{c_G} See help for available tools with {__}iPythonProjectConfiguration(){_}" ]

            exec_lines += [ f"print({repr(x)})" ]

            # TODO add imports for project configuration tool

        except ValueError:
            pass
        except Exception as E:
            x = ERR("Errors reading from config file")
            err_lines += [ f"print({repr(x)})", str(E) ]

    #-----------------------------------------------------------------------------#
    #   Create empty config file if python project is detected and non existing   #
    #-----------------------------------------------------------------------------#

    if create_project_config and project_directory and not project_config_file:
        project_config_file = join( project_directory, '.ipython_startup.py' )
        try:
            conf.writeFile()
            x = f"{c_W}      Created empty config file - {c_C}{project_config_file}{c_G}\n        - reload to load tool module"
            exec_lines += [ f"print(\"{repr(x)}\")" ]
        except:
            ERR(f"Couldn't create config file - {c_C}{project_directory}")
            err_lines += [ f"print(\"{repr(x)}\")" ]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#   KEEP ABOVE CODE AT THE TOP OF THIS FILE                                   #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#=============================================================================#
#   Lines of code to run at IPython startup                                   #
#       [ default = [] ]                                                      #
#-----------------------------------------------------------------------------#

c.InteractiveShellApp.exec_lines = [ *exec_lines,
                                     *USER_ADDED,
                                     *err_lines ]

#-----------------------------------------------------------------------------#
# TerminalIPythonApp(BaseIPythonApplication,InteractiveShellApp) config       #
#-----------------------------------------------------------------------------#

#  See also: BaseIPythonApplication.add_ipython_dir_to_sys_path
# c.TerminalIPythonApp.add_ipython_dir_to_sys_path = False

## Execute the given command string.
#  See also: InteractiveShellApp.code_to_run
# c.TerminalIPythonApp.code_to_run = ''

## Whether to install the default config files into the profile dir.
#  See also: BaseIPythonApplication.copy_config_files
# c.TerminalIPythonApp.copy_config_files = False

## Whether to display a banner upon starting IPython.
#  Default: True
# c.TerminalIPythonApp.display_banner = True

## Run the file referenced by the PYTHONSTARTUP environment
#  See also: InteractiveShellApp.exec_PYTHONSTARTUP
# c.TerminalIPythonApp.exec_PYTHONSTARTUP = True

## List of files to run at IPython startup.
#  See also: InteractiveShellApp.exec_files
# c.TerminalIPythonApp.exec_files = []

## lines of code to run at IPython startup.
#  See also: InteractiveShellApp.exec_lines
# c.TerminalIPythonApp.exec_lines = []

## A list of dotted module names of IPython extensions to load.
#  See also: InteractiveShellApp.extensions
# c.TerminalIPythonApp.extensions = []

## Path to an extra config file to load.
#  See also: BaseIPythonApplication.extra_config_file
# c.TerminalIPythonApp.extra_config_file = ''

## A file to be run
#  See also: InteractiveShellApp.file_to_run
# c.TerminalIPythonApp.file_to_run = ''

## Enable GUI event loop integration with any of ('asyncio', 'glut', 'gtk',
#  'gtk2', 'gtk3', 'gtk4', 'osx', 'pyglet', 'qt', 'qt4', 'qt5', 'qt6', 'tk',
#  'wx', 'gtk2', 'qt4').
#  See also: InteractiveShellApp.gui
# c.TerminalIPythonApp.gui = None
