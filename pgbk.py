#!/usr/bin/python

#----------------------------------------------------------------------
# Be sure to add the python path that points to the LLDB shared library.
#
# # To use this in the embedded python interpreter using "lldb" just
# import it with the full path using the "command script import"
# command
#   (lldb) command script import /path/to/file.py
#
# Inspired by 
# http://llvm.org/svn/llvm-project/lldb/trunk/examples/python/cmdtemplate.py
# 
# For a blog post describing this, visit 
# https://aijaz.net/2017/01/11/lldb-python/
#----------------------------------------------------------------------

import lldb
import commands
import codecs
import optparse
import shlex

def __lldb_init_module(debugger, dict):
    # This initializer is being run from LLDB in the embedded command interpreter
    # Make the options so we can generate the help text for the new LLDB
    # command line command prior to registering it with LLDB below
    parser = create_pgbk_options()
    pgbk_command.__doc__ = parser.format_help()

    # Add any commands contained in this module to LLDB
    debugger.HandleCommand('command script add -f pgbk.pgbk_command pgbk')

    print """The "pgbk" command has been installed, \
    type "help pgbk" or "pgbk --help" for detailed help.\
    """

def create_pgbk_options():
    """Parse the options passed to the command. 
    Also provides the description string that's used as
    the command's help string.
    """
    usage = "usage: %prog <variable_name>"
    description = '''This command will run the jq using jq_filter on the
NSString local variable variable_name, which is expected to contain valid JSON. 
As a side effect, the JSON contained in variable_name will be saved in
/tmp/jq_json and the filter will be saved in /tmp/jq_prog.

Example:
%prog '.[]|{firstName, lastName}' jsonStr
%prog '.[]|select(.id=="f9a5282e-523f-4b83-a6ca-566e3746a4c7").schools[1].\
school.mainLocation.address.city' body
'''
    parser = optparse.OptionParser(
        description=description,
        prog='pgbk',
        usage=usage)
    return parser

# The actual python function that is bound to the lldb command.
def pgbk_command(debugger, command, result, dict):
    # in a command - the lldb.* convenience variables are not to be used
    # and their values (if any) are undefined
    # this is the best practice to access those objects from within a command
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()
    if not frame.IsValid():
        return "no frame here"

    val = frame.var(args[1])
    val_string = val.GetObjectDescription()

    u = val_string.encode("gb2312")

    # invoke pgbk and print the output to the result variable
    print >> result, (commands.getoutput("%s" % (u) ))

    # not returning anything is akin to returning success
