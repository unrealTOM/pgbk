#!/usr/bin/python

#---------------usage--------------
# put this file to home directory ~
# open terminal, type without quote "echo command script import ~/pgbk.py >> ~/.lldbinit
# restart xcode, when breakpoint hit, call: pgbk $var
#--------------------------------------------------------------------

import sys
import lldb
import commands
import codecs
import optparse
import shlex

def __lldb_init_module(debugger, dict):
    parser = create_pgbk_options()
    pgbk_command.__doc__ = parser.format_help()

    reload(sys)
    sys.setdefaultencoding('gbk')

    # Add any commands contained in this module to LLDB
    debugger.HandleCommand('command script add -f pgbk.pgbk_command pgbk')

    print """The "pgbk" command has been installed, \
    type "help pgbk" or "pgbk --help" for detailed help.\
    """


def create_pgbk_options():
    usage = "usage: pgbk <variable_name>"
    description = '''This command will print gbk encoded string to readable format.'''
    parser = optparse.OptionParser(description=description, prog='pgbk', usage=usage)
    return parser


#### The actual python function that is bound to the lldb command.
def pgbk_command(debugger, command, result, dict):
    command_args = shlex.split(command)
    parser = create_pgbk_options()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        print >>result, "parsing error!"
        return

    if len(args) < 1:
        print >>result, "empty arguments!"
        return

    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()
    if not frame.IsValid():
        return "no frame here"

    val = frame.var(args[0])
    val_string = val.GetSummary()

    print(val_string.encode('utf8'))

