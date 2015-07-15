import sys

def set_flags():
    """ Sets the various flags specified by a user """
    #if no file
    if len(sys.argv) == 1:
        print "You need to specifiy a file to read!"
        quit()

    out = sys.argv[2]

    #debug?
    if "d" in sys.argv or "debug" in sys.argv:
        textout = True
    else:
        textout = False

    #aa or ua
    if "aa" in sys.argv:
        aa = True
    else:
        aa = False

    return textout,aa,out