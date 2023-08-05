import os
import datetime
import __main__


##############################################################################
# GLOBALS

SCRIPTPATH = os.path.abspath(__main__.__file__ if hasattr(__main__, "__file__") else ".")
SCRIPTDIR = os.path.dirname(SCRIPTPATH)
MODULEPATH = os.path.abspath(__file__)
MODULEDIR = os.path.dirname(MODULEPATH)


##############################################################################
# TIMESTAMP

def epochstring():
    return "0000-00-00 00:00:00.000000 +0000"

def nowstring():
    timestamp = datetime.datetime.now(tz=datetime.timezone.utc).astimezone()

    return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f %z")


##############################################################################
# DICTMERGE

def dictmerge(dict1, dict2):
    """
        Recursively merge dict2 into dict1.
    """

    for key, value in dict2.items():
        if   key in dict1 and hasattr(dict1[key], "items") and hasattr(dict2[key], "items"):
            dictmerge(dict1[key], dict2[key])
        else:
            dict1[key] = value

    return dict1

