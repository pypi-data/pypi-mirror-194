__version__ = "0.0.2"

from .ipythonprojectfunctions import setup, ProjectConfiguration


def main(arg = None, *, config_path = None):
    """
    main( *, func, config_path = None )
      - simple way of getting ProjectConfiguration methods

        *args       = method(s) to return
                        - takes precedence over config_path
        config_path = path to .ipython_startup.py

        func options:
            - 'addline'
            - 'class'
            - 'class-help'
            - 'emptystart'
            - 'findlock'
            - 'getfile'
            - 'getlines'
            - 'help'
            - 'initconfig'
            - 'rmline'
            - 'writefile'

        Returns path to .ipython_startup.py if existing, else None, if
      no argument is given.

    """
    _W  = "\x1b[0;1;37m"
    _R  = "\x1b[0;1;31m"
    _G  = "\x1b[0;2;37m"
    _g  = "\x1b[0;0;37m"
    _GI = "\x1b[0;2;37;3m"
    _gi = "\x1b[0;0;37;3m"
    _U  = "\x1b[4m"
    _   = "\x1b[0m"

    funcs = { 'addline'   : ProjectConfiguration.addLine,
              'class'     : ProjectConfiguration,
              'class-help': ProjectConfiguration.help,
              'emptystart': ProjectConfiguration.emptyStartup,
              'findlock'  : ProjectConfiguration.findLockDir,
              'getfile'   : ProjectConfiguration.getFile,
              'getlines'  : ProjectConfiguration.getLines,
              'help'      : helpMsg,
              'initconfig': ProjectConfiguration.ipythonInitConfig,
              'rmline'    : ProjectConfiguration.rmLine,
              'writefile' : ProjectConfiguration.writeFile  }

    def helpMsg(_all = False):

        msg = [ '', f"{_W}  {_U}BB_iPythonTools{_GI}",
                f" - import tools for iPython shells{_}",
                '', f"{_W}    >>>{_g} main({_G} 'help'{_} )",
                f"{_gi}        - returns requested method{_}",
                '', f"{_C}  Available functions:{_}", '' ]

        for k, v in funcs.items():
            if k == 'help':
                msg += [f"{_gi}    {"'"+k+"'":>15}{_W} >>{_G} this help message{_}"]
            elif k == 'class-help':
                msg += [f"{_gi}    {"'"+k+"'":>15}{_W} >>{_G} ProjectConfiguration's help message{_}"]
            else:
                msg += [f"{_gi}    {"'"+k+"'":>15}{_W} >>{_G} {v.__name__}{_}"]

        return '\n'.join([ *msg, '' ])

    project_config_file = setup(config_path)

    if not arg:
        return project_config_file

    try:
        if arg in ( 'help', 'class-help' ):
            print( funcs[arg]() )
            return
        else:
            return funcs[arg]
    except:
        print(f"{_R}  [ERROR]{_GI} invalid function - use main('help') for list")
        return
