
import json
import time
import hashlib

import requests

import gzip

#from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout 

from . import s_log , s_config , s_util

#####################################################################

def client_job_set( payload_dict ) :

    #time.sleep( 1 )

    #s_log.write( payload_dict )

    payload_json = s_util.json_encode( payload_dict )
    #s_log.write( payload_json )

    payload = gzip.compress( bytes( payload_json , "utf-8" ) )
    #plain_string_again = gzip.decompress(compressed_value)

    #####################################################################

    mw = mw_get( )
    if(not mw): return(False)

    #####################################################################

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "omniclient" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Channel": s_config.get_key( "endpoint/channel" ) ,
                    "X-Omni-Action": "clientjobset" ,
                }

    if endpoint_host != None and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers , payload )

    if(res==False):
        s_log.write("res??")
        return(False)

    s_log.write( str(res.headers ))


    if( not "X-Omni-Jid" in res.headers ) :
        s_log.write( "Not found X-Omni-Jid" )
        return( False )

    if( len( res.headers[ "X-Omni-Jid" ] ) != 67 ) :
        s_log.write( "X-Omni-Jid!=67" )
        return( False )

    jid = res.headers[ "X-Omni-Jid" ]

    return( jid )

#####################################################################

def client_job_get( jid ) :

    #time.sleep(1)
    #####################################################################

    mw = mw_get( )
    if(not mw): return(False)

    #####################################################################

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "omniclient" ,
                    "X-Omni-Mw": mw ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Action": "clientjobget" ,
                    "X-Omni-Jid": jid ,
                }

    if endpoint_host != None  and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers )

    if(res==False):
        s_log.write("res??")
        return(False)

    s_log.write( str(res.headers ) )


    if( not "X-Omni-State" in res.headers ) :
        s_log.write( "Not found X-Omni-State" )
        return( False )

    if(res.headers["X-Omni-State"]!="done") :
        s_log.write( "Not Done X-Omni-State" )
        return( None )


    payload=json.loads(gzip.decompress(res.content))

    s_log.write(payload)

    return( payload )

#####################################################################

def mw_get( ) :
    mw1=get_mw()
    if(mw1==False):
        s_log.write("client_job_set mw???")
        return(False)
    mw = "MWCf068980781d390b52666900ee6d4cce11ac2e9e8e175a9c3293e35659911df5a" + mw1
    mw = "MWH" + hashlib.sha256( mw.encode( "utf-8" ) ).hexdigest( )
    s_log.write(mw)
    return( mw )



def get_request_response( request_headers , payload="" ) :

    endpoint_sslverify = s_config.get_key( "endpoint/sslverify" )

    if endpoint_sslverify == None :
        endpoint_sslverify = True
    else :        
        if endpoint_sslverify == "yes":
            endpoint_sslverify = True
        else :
            endpoint_sslverify = False

    endpoint_timeout = s_config.get_key( "endpoint/timeout" )
    if endpoint_timeout == None or ( not endpoint_timeout.isdigit( ) ) :
        endpoint_timeout = 5
    else:
        endpoint_timeout = int( endpoint_timeout )

    endpoint_url = s_config.get_key( "endpoint/url" )

    #####################################################################

    try :
        response = requests.post( endpoint_url , data = payload , headers = request_headers , timeout = endpoint_timeout , verify = endpoint_sslverify )
    except requests.exceptions.SSLError as e :
        s_log.write( "requests.exceptions.SSLError:"+str(e) )
        return( False )    
    except requests.exceptions.ReadTimeout as e :
        s_log.write( "requests.exceptions.ReadTimeout:"+str(e) )
        return( False )    
    except requests.exceptions.ConnectionError as e :
        s_log.write( "requests.exceptions.ConnectionError::"+str(e) )
        s_log.write( "Maybe no omnibus..?" )
        s_log.write( endpoint_url )
        s_log.write( headers )
        return( False )  


    return( response )


def get_mw( ) :

    endpoint_host = s_config.get_key( "endpoint/host" )
    endpoint_token = s_config.get_key( "endpoint/token" )

    headers =   {
                    "User-Agent" : "omniclient" ,
                    "X-Omni-Authorization": endpoint_token ,
                    "X-Omni-Action": "mwget" ,
                }

    if endpoint_host != None  and endpoint_host != "" :
        headers[ "Host" ] = endpoint_host

    #s_log.write( headers )

    res = get_request_response( headers )

    if( res == False ) :
        s_log.write( "get_mw false res" )
        return( False )

    #s_log.write(str(res.headers))

    if( not "X-Omni-Mw" in res.headers ) :
        s_log.write( "Not found X-Omni-Mw" )
        return( False )

    if( len( res.headers[ "X-Omni-Mw" ] ) != 67 ) :
        s_log.write( "X-Omni-Mw!=67" )
        return( False )

    mw = res.headers[ "X-Omni-Mw" ]

    #s_log.write(mw)

    return( mw )




#####################################################################



 

    