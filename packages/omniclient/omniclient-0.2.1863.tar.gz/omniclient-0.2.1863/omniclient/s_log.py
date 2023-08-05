
import os
import json
from datetime import datetime
from . import s_config 

#####################################################################

log_filepath = False

def default_json( t ) :
    return f'{t}'

def write( msg_raw , context = "" ) :

    global log_filepath

    log_workspacedir = s_config.get_key( "sys/workspacedir" , "/tmp")

    # FIXME TODO
    os.makedirs( log_workspacedir , exist_ok = True )

    # Add trailing slash
    log_filepath = os.path.join(log_workspacedir, "") + "omniclient.log" 

    if( context != "" ) : context = "[" + context + "] "

    msg = msg_raw

    if( msg == None ) : msg = "!NONE!"
    
    if( isinstance( msg , list ) ) :
        msg = ",".join( map( str , msg ) )
    
    if( isinstance( msg , dict ) ) :
        # FIXME TODO use util json note numpy stuff
        msg = json.dumps( msg , default = default_json , indent=4, sort_keys=True)

    if( isinstance( msg , ( int , float , bool ) ) ) :
        msg = str( msg )

    msg = datetime.now( ).strftime( "%Y_%m_%d-%I_%M_%S_%p" ) + " " + context + msg
    with open( log_filepath , "a+" , 1 ) as log_file :
        log_file.write( msg + "\n" )

def flush( ) :
    if os.path.isfile( log_filepath ) :
        os.remove( log_filepath )

