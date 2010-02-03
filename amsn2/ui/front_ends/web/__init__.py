
from amsn2.core import aMSNUserInterfaceManager
import sys

# Here we load the actual front end.
# We need to import the front end module and return it
# so the guimanager can access its classes
def load():
    try:
        import web
    except ImportError, e:
        etype, value, tb = sys.exc_info()
        traceback.print_exception(etype, value, tb.tb_next)
        return None
    return web

# Initialize the front end by checking for any
# dependency then register it to the guimanager
try:
    import imp
    aMSNUserInterfaceManager.register_frontend("web", sys.modules[__name__])

except ImportError:
    pass

