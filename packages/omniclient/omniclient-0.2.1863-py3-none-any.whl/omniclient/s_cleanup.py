
import atexit

#####################################################################

from . import s_log  

#####################################################################

def cleanup( ) :
    s_log.write_msg( "CLEANUP" )

atexit.register( cleanup )
s_log.write_msg( "Registered cleanup" )



    