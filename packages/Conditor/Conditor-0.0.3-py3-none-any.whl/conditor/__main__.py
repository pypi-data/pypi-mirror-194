import sys
import os

import conditor.cli

def main(cwd=None, argv=None) :
    if cwd is None :
        cwd = os.getcwd()
    if argv is None :
        argv = sys.argv
        pass
    #print(cwd, argv)
    conditor.cli.cmd_conditor_eval()
    return

if __name__ == '__main__' :
    main()
    pass

