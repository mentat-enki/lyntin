#!/usr/bin/env python
#######################################################################
# This file is part of Lyntin.
# copyright (c) Free Software Foundation 2001, 2002
#
# Lyntin is distributed under the GNU General Public License license.  See the
# file LICENSE for distribution details.
# $Id: lyntintk.pyw,v 1.2 2003/05/27 02:06:39 willhelm Exp $
#######################################################################
"""
This module holds the Lyntin "global variables" and constants as well
as the main function which starts Lyntin off.
"""

def shutdown():
  """
  This gets called by the Python interpreter atexit.  The reason
  we do shutdown stuff here is we're more likely to catch things
  here than we are to let everything cycle through the 
  ShutdownEvent.  This should probably get fixed up at some point
  in the future.
  """
  import lyntin.hooks, lyntin.exported
  try:
    lyntin.exported.write_message("shutting down...  goodbye.")
  except:
    print "shutting down...  goodbye."
  lyntin.hooks.shutdown_hook.spamhook(())

if __name__ == '__main__':
  try:
    import sys, os
    from lyntin import engine, event, utils, __init__

    # read through options and arguments
    optlist = utils.parse_args(sys.argv[1:])

    for mem in optlist:
      if mem[0] == '--ui' or mem[0] == '-u':
        __init__.options['ui'] = mem[1]

      elif mem[0] == '--readfile' or mem[0] == "--read" or mem[0] == '-r':
        __init__.options['readfile'].append(mem[1])

      elif mem[0] == '--moduledir' or mem[0] == '-m':
        d = mem[1]
        if d[-1] != os.sep:
          d = mem[1] + os.sep
        __init__.options['moduledir'].append(d)

      elif mem[0] == '--datadir' or mem[0] == '-d':
        d = mem[1]
        if d[-1] != os.sep:
          d = mem[1] + "/"
        __init__.options['datadir'] = d

      elif mem[0] == '--nosnoop':
        __init__.options['snoopdefault'] = 0

      elif mem[0] == '--help':
        print constants.HELPTEXT
        sys.exit(0)

      elif mem[0] == '--version':
        print constants.VERSION
        sys.exit(0)

      else:
        opt = mem[0]
        while len(opt) > 0 and opt[0] == "-":
          opt = opt[1:]

        if len(opt) > 0:
          if __init__.options.has_key(opt):
            __init__.options[opt].append(mem[1])
          else:
            __init__.options[opt] = [mem[1]]

    # if they haven't set the datadir via the command line, then
    # we go see if they have a HOME in their environment variables....
    datadir = __init__.options['datadir']
    if not datadir:
      if os.environ.has_key("HOME"):
        datadir = os.environ["HOME"]
        if len(datadir) > 0:
          if datadir[-1] != os.sep: 
            datadir = datadir + os.sep

      __init__.options['datadir'] = datadir

    import atexit
    atexit.register(shutdown)

    # instantiate an engine
    engine.myengine = engine.Engine()
    engine.myengine.initialize()

    # generate a startup event.
    # StartupEvent handles all the rest of the initialization
    # including parsing command-line arguments and such.
    event.StartupEvent().enqueue()

    # start the engine which will execute the startupevent
    # and start executing.
    engine.myengine.runengine()

  except SystemExit:
    if engine.myengine != None:
      event.ShutdownEvent().enqueue()
      engine.myengine.runengine()
    
  except:
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Local variables:
# mode:python
# py-indent-offset:2
# tab-width:2
# End:
