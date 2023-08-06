
import argparse
import pathlib
import os

import conditor

def cmd_conditor_eval() :
    parser = argparse.ArgumentParser(
        description = 'Conditor Command Description'
    )
    parser.add_argument('--cwd',
        type = pathlib.Path,
        default = os.getcwd()
    )
    parser.add_argument('inst',
        type = str
    )
    args = parser.parse_args()
    ctx = conditor.get_ctx(args.cwd)
    inst = args.inst
    print(repr(ctx.eval(inst)))
    return


