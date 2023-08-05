__version__ = "0.0.1"

from .ipythonprojectfunctions import setup, ProjectConfiguration

project_config_file = None

def main(*args, config_path = None):
    """
    main( *, func, config_path = None )
      - simple way of getting ProjectConfiguration methods

        *args       = method(s) to return
                        - takes precedence over config_path
        config_path = path to .ipython_startup.py

        func options:
            - 'addline'
            - 'rmline'
            - 'getlines'
            - 'getfile'
            - 'writefile'
            - 'initconfig'

    """
    global project_config_file

    if not args:
        if not project_config_file:
            project_config_file = setup(config_path)
        return ProjectConfiguration

    funcs = { 'addline'   : ProjectConfiguration.addLine,
              'rmline'    : ProjectConfiguration.rmLine,
              'getlines'  : ProjectConfiguration.getLines,
              'getfile'   : ProjectConfiguration.getFile,
              'writefile' : ProjectConfiguration.writeFile,
              'initconfig': ProjectConfiguration.ipythonInitConfig,
              'findlock'  : ProjectConfiguration.findLockDir,
              'emptystart': ProjectConfiguration.emptyStartup }

    R = []
    for i in args:
        if i in funcs:
            R += funcs[i]

    if len(R) == 1:
        return R[0]
    return R
