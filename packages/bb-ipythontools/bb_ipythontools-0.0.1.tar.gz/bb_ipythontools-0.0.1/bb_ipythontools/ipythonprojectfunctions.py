import os, sys, shutil
from importlib.resources import files as source
from os.path import ( dirname as DN,
                      basename as BN,
                      isfile,
                      isdir,
                      splitext,
                      join as JN,
                      expanduser )
from operator import itemgetter
import logging
log = logging.getLogger(__name__)

from . import datafiles

# colors
c_G  = '\x1b[0;2;37;3m'     # gray       <i>
c_W  = '\x1b[0;1;37m'       # white
c_C  = '\x1b[0;0;36;3m'     # cyan       <i>
c_g  = '\x1b[0;0;32m'       # green
c_gr = '\x1b[0;2;32;3m'     # darkgreen  <i>
c_P  = '\x1b[0;0;35;3m'     # purple     <i>
c_B  = '\x1b[0;1;34;3m'     # blue       <i>
c_R  = '\x1b[0;1;31m'       # red
c_Y  = '\x1b[0;1;33m'       # yellow
___  = '\x1b[0;0;37;3m'     # light gray <i>
__   = '\x1b[0;0;37m'       # light gray
_    = '\x1b[0m'            # RESET
project_config_file = None
project = None
TTY = sys.stdin.isatty()

def setup(config = None):
    global project_config_file
    global project

    if config and isfile(config):
        project_config_file = config
    else:
        ldir, pfile = ProjectConfiguration.findLockDir()
        if pfile:
            project_config_file = pfile
        elif ldir:
            project_config_file = JN( ldir, '.ipython_startup.py' )
            with open( project_config_file, 'w' ) as f:
                f.write( ProjectConfiguration.emptyStartup() )
        else:
            return None

    project = BN(DN( project_config_file ))
    return project_config_file

class ProjectConfiguration:
    """
    ProjectConfiguration
      - Configure .ipython_startup.py located in project directory

        The .iPython_startup.py file is read when loading iPython from
      anywhere in a projects folder heirarchy if BB-iPythonTools are
      installed and setup. BB-iPythonTools will automatically add the
      project config file to the root of the project by looking for a
      lock file. This file can be added anywhere manually with the class
      function ProjectConfiguration.writeProjectStartupFile() and can be
      returned with ProjectConfiguration.getProjectStartupFile().

        These class methods are retrieved through an outside function,
      main(), which python_config.py uses to set longer aliases for each
      class so as to not pollute the namespace of iPython. The __doc__
      strings are titled using these aliases.

        cls.addLine()   << - addProjectStartupLine()
        cls.rmLine()    << - rmProjectStartupLine()
        cls.getLines()  << - getProjectStartupLines()
        cls.getFile()   << - getProjectStartupFile()
        cls.writeFile() << - writeProjectStartupFile()

        The argument 'help' can be passed to any of these methods to print
      all the doc strings in this class.

    """

    @classmethod
    def findLockDir(cls, *args):
        """
        findLockDir()
          - Attempt to find lockfile to determine project's root directory

            Returns ( lockfile_dir, .ipython_startup.py )

          *args:
            'help' = print( cls.help )

        """
        if 'help' in args:
            return cls.help()

        cd = os.getcwd()
        HOME = expanduser('~')
        pf = None
        lf = None
        while True:
            try:
                lf = glob( '*.lock', root_dir = cd )[0]
                lockfile = join( cd, lf )
            except:
                lf = None

            try:
                pf = join( cd, '.ipython_startup.py' )
                assert isfile(pf)
            except:
                pf = None

            if lf:
                return cd, pf
            elif cd == HOME:
                return None, pf
            elif not os.access( cd, os.W_OK ):
                return None, pf
            else:
                cd = DN( cd )

    @classmethod
    def emptyStartup(cls):
        """
        emptyStartup():
          - Return an empty startup file as a string

            .ipython_startup.py template

          *args:
            'help' = print( cls.help )

        """
        if 'help' in args:
            return cls.help()

        if not project_config_file:
            return

        pcf = '\n'.join([ "# Project configuration file",
                          "#",
                          "#    Lines in this file will be added to ipython's configuration",
                          "#  module 'InteractiveShellApp.exec_lines' to be loaded at startup\n" ])

        return pcf

    @classmethod
    def addLine(cls, line = None, *args):
        """
        addProjectStartupLine( line = None )
          - Add a line to .ipython_startup.py

            line = Exec line to add to project's startup file for iPython
                - user will be prompted before any changes
                - if None, user will be prompted to enter text

          *args:
            'help' = print( cls.help )

        """
        if 'help' in args:
            return cls.help()

        if not project_config_file:
            print( f"{c_R}\n  [ERROR]{c_G} Config file path is not set{_}" )
        elif not isfile( project_config_file ):
            print( f"{c_R}\n  [ERROR]{c_G} Config file '{project_config_file}' doesn't exist{_}" )

        if not line:
            line = repr(input( f"{__}  Input line to execute at startup:{c_W}\n\n    >>>{_} " ))
        _A = input( f"\n{__}  Add this line to {project}'s iPython startup file?{c_W}\n\n    (Y,n)>{_} " )
        if _A.lower() not in ('y', 'yes'):
            print( f"{c_R}  Cancelled adding line{_}\n" )
            return
        _A = input( f"\n{__}  Would you like to test exec() on this line now?{c_G}\n    - >> {c_B}exec({__}'{newline}'){c_W}\n\n    (Y,n)>{_} " )
        if _A.lower() in ('y', 'yes'):
            try:
                exec(newline)
            except Exception as E:
                print( f"{c_R}\n  [ERROR]{c_G} failed to execute command{_}\n" )
                _A = input( f"{c_W}    View traceback? (Y,n)>{_} " )
                if _A in ('y', 'yes'):
                    log.exception(E)
                return
        with open( project_config_file, 'a' ) as f:
            f.write( line + '\n' )
        print( f"{c_W}    Added line to{c_C} {project}'s iPython startup file{_}\n" )

    @classmethod
    def rmLine(cls, line = None, *args):
        """
        rmProjectStartupLine( line = None )
          - Remove line from .ipython_startup.py

            line = Line or part of line to be removed
                - user will be prompted before any changes
                - if None, user will be prompted to enter text

          *args:
            'help' = print( cls.help )

        """
        if 'help' in args:
            return cls.help()

        if not project_config_file:
            print( f"{c_R}\n  [ERROR]{c_G} Config file path is not set{_}" )
        elif not isfile( project_config_file ):
            print( f"{c_R}\n  [ERROR]{c_G} Config file '{project_config_file}' doesn't exist{_}" )

        rmlines = []
        with open( project_config_file, 'r', errors = 'ignore' ) as f:
            orig = f.read().split('\n')

        lines = list(filter( None, [ i if not i.strip().startswith('#') else None for i in orig ]))
        if not line:
            line = input( f"{__}  Input line, start of line, or line number to remove from startup:{c_W}\n    >>>{_}" )
        if line.isnumeric() and int(line) >= 0 and int(line) < len(lines):
            rmlines = [ lines[int(line)] ]
        else:
            for i in lines:
                rmlines.append({ 'line'      : i,
                                 'startsWith': True if i.startswith(line) else False,
                                 'foundIn'   : True if line in i else False })
                if not rmlines['startsWith'] and not rmlines['foundIn']:
                    rmlines.pop(-1)

        if not rmlines:
            print( f"{c_R}\n  No matches found for {__}'{line}'{_}\n" )
            return

        rmlines = sorted( rmlines, key = itemgetter( 'startsWith', 'foundIn' ), reverse = True )
        A_ = 'n'
        while rmlines and A_ not in ('y', 'yes', 'c', 'cancel'):
            print( f"{c_W}  Remove this line from {project}'s startup file?{c_W}\n    >{c_C} {rmlines[0]['line']}\n")
            A_ = input( f"{c_W}    (Y,n,c)>{_} " )

        if A_.lower() not in ('y', 'yes'):
            print( f"{c_R}\n  No changes have been made - exiting...{_}\n" )
            return
        else:
            i = orig.index( rmlines[0]['line'] )
            rm = orig.pop(i)

            with open( project_config_file, 'w' ) as f:
                f.write(orig)
            print( f"{__}\n  Line...{c_W}\n    >{c_G} {rm}{c_W} <{__}\n      ...has been removed from {project}'s iPython startup file{c_B}\n    - exiting now...{_}\n" )

    @classmethod
    def getLines(cls, *args):
        """
        getProjectStartupLines()
          - View executed lines in .ipython_startup.py

          *args:
            'help' = print( cls.help )

        """
        if 'help' in args:
            return cls.help()

        if not project_config_file:
            if 'list' in args:
                return []
            else:
                print( f"{c_R}\n  [ERROR]{c_G} Config file path is not set{_}" )
                return
        elif not isfile( project_config_file ):
            if 'list' in args:
                return []
            else:
                print( f"{c_R}\n  [ERROR]{c_G} Config file '{project_config_file}' doesn't exist{_}" )
                return

        with open( project_config_file, 'r', errors = 'ignore' ) as f:
            lines = list(filter( None, [ i if not i.strip().startswith('#') else None for i in f.read().strip().split('\n') ]))
        c = 0
        _list, _lines = [], []
        print(f"{c_W}  Startup exec lines for {project}:{_}\n")
        for i in lines:
            _lines += [i]
            _list += [ f"{c_C}{c:>6}){__} {i}{_}" ]
            c += 1

        if 'list' in args:
            return _lines

        print( '\n'.join(_list) + '\n' )

    @classmethod
    def getFile(cls, *args):
        """
        getProjectStartupFile()
          - Returns .ipython_startup.py file as a string

          *args:
            'help' = print( cls.help )

        """
        global project_config_file
        if 'help' in args:
            return cls.help()

        if not project_config_file:
            lockdir, startfile = cls.findLockDir()
            if startfile:
                project_config_file = startfile
                with open( startfile, 'r' ) as f:
                    R = f.read()
            else:
                print(f"{c_R}  [ERROR]{c_G} .ipython_startup.py could not be found{_}")
                return ""
        else:
            with open( project_config_file, 'r' ) as f:
                R = f.read()

        if 'path' in args:
            return project_config_file

        return R

    @classmethod
    def writeFile(cls, _dir = None, *args):
        """
        writeProjectStartupFile()
          - Writes file to disk

            _dir = directory to write file in
                - defaults to None
                - when None, attempts to find project root

          *args:
            'help' = print( cls.help )

            If file exists, and _dir is given, then the existing file will
          be moved to .ipython_startup.old. Returns True if successfully
          written and False otherwise.

        """
        if 'help' in args:
            return cls.help()

        ps = None
        if _dir:
            if not isdir(_dir):
                print(f"{c_R}\n  [ERROR]{c_G} Directory '{_dir}' doesn't exist{_}\n")
                return False
            elif isfile(JN( _dir, '.ipython_startup.py' )):
                ps = JN( _dir, '.ipython_startup.py' )
                print(f"{c_Y}\n  [WARNING]{c_G} '{ps}' already exists\n{__}              - moving existing file to '.ipython_startup.old'{_}\n")
                osOld = splitext(ps)[0] + '.old'
                shutil.move( ps, psOld )
        else:
            lockfile, startfile = cls.findLockDir()
            if not lockfile:
                print(f"{c_R}\n  [ERROR]{c_G} Couldn't determine projects root directory{_}")
                return False
            _dir = dirname(lockfile)
            ps = JN( _dir, '.ipython_startup.py' )

            if isfile(ps):
                if sys.stdin.isatty():
                    print(f"{c_Y}\n  [WARNING]{c_G} '{ps}' already exists{_}\n")

                return False

        if not os.access( _dir, os.W_OK ):
            if sys.stdin.isatty():
                print(f"{c_R}\n  [ERROR]{c_G} User doesn't have write permissions to '{cdir}'{_}\n")

            return False

        with open( ps, 'w' ) as f:
            f.write( cls.emptyStartup )

        if sys.stdin.isatty():
            print( f"{c_W}\n  Wrote file to '{c_C}{ps}{c_W}'{_}\n" )

        return True

    @classmethod
    def ipythonInitConfig(cls, profile = None, *args, link = None):
        """
        ipythonInitConfig( profile )
          - Write/replace ipython_config.py found in $HOME/.ipython

          *args:
            profile = name or absolute path of user's iPython profile
            'help'  = print( cls.help )

          **kwargs:

        """
        if 'help' in args:
            return cls.help()

        msg = '\n'.join([ f"{c_W}  BB-iPythonTools{_}",
                          '',
                          f"{__}      This will replace or create a ipython_config.py in the",
                          f"    user's provided profile. This can either be an absolute path",
                          "    to the user's profile directory, or just the name of the profile.",
                          "    This will attempt to auto format the name and, unless the profile",
                          "    argument is an absolute directory, will place the file in the",
                          "    standard location. If a current file already exists, the existing",
                          f"    file will be moved to 'python_config.old'.{_}" ])
        print( f"\n{msg}\n\n{c_W}    Write config to '{pf}'?" )
        A_ = input( f"        (Y,n)>{_} " )

    @classmethod
    def help(cls):
        mods = [ cls.__doc__.split('\n'),
                 cls.emptyStartup.__doc__.split('\n'),
                 cls.findLockDir.__doc__.split('\n'),
                 cls.addLine.__doc__.split('\n'),
                 cls.rmLine.__doc__.split('\n'),
                 cls.getLines.__doc__.split('\n'),
                 cls.getFile.__doc__.split('\n'),
                 cls.writeFile.__doc__.split('\n'),
                 cls.ipythonInitConfig.__doc__.split('\n') ]

        wid = os.get_terminal_size().columns - 24
        msg, lines = [], []
        M = 0
        while mods:
            lines.append( mods.pop(0) )
            c = 0
            if msg:
                msg += [f"\n    {c_C}{'':-<{wid}}{_}"]
            while c < len(lines[M]):
                if c == 1:
                    lines[M][c] = f"{c_W}{lines[M][c]}".replace('( line = None )',f"{c_W}({__} line{c_g} ={c_gr} None{c_W} ){_}").replace('( profile )',f"{c_W}({__} profile{c_W} ){_}")
                elif c == 2:
                    lines[M][c] = f"{___}{lines[M][c]}{_}"
                elif lines[M][c].strip().startswith('-'):
                    lines[M][c] = f"{c_G}{lines[M][c]}{_}"

                if '.ipython_startup.py' in lines[M][c]:
                    _c = _ if c > 2 else c_G
                    lines[M][c] = lines[M][c].replace('.ipython_startup.py',f"{c_C}.ipython_startup.py{_c}")
                elif '.ipython_startup.old' in lines[M][c]:
                    _c = _ if c > 2 else c_G
                    lines[M][c] = lines[M][c].replace('.ipython_startup.old',f"{c_C}.ipython_startup.old{_c}")
                elif '.ipython_config.py' in lines[M][c]:
                    _c = _ if c > 2 else c_G
                    lines[M][c] = lines[M][c].replace('.ipython_config.py',f"{c_C}.ipython_config.py{_c}")
                elif '.ipython_config.old' in lines[M][c]:
                    _c = _ if c > 2 else c_G
                    lines[M][c] = lines[M][c].replace('.ipython_config.old',f"{c_C}.ipython_config.old{_c}")
                elif '$HOME/.ipython' in lines[M][c]:
                    _c = _ if c > 2 else c_G
                    lines[M][c] = lines[M][c].replace('$HOME/.ipython',f"{c_C}$HOME/.ipython{_c}")

                if '*args:' in lines[M][c]:
                    lines[M][c] = lines[M][c].replace('*args:', f"{c_C}*{c_W}args:{_}" )

                msg.append( lines[M][c] )

                c += 1
            M += 1

        print( '\n'.join(msg) )
