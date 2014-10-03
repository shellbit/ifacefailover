import os, sys
from serializationUtil import serialize
from verifier.icmpRouteVerifier import IcmpRouteVerifier
from handler.httpHandler import HttpHandler
from handler.fonaRaspberryPiHandler import FonaRaspberryPiHandler
from handler.logHandler import LogHandler

dir=sys.argv[1]
if not os.path.exists(dir):
    os.makedirs(dir)

filelist = [ f for f in os.listdir(dir) if f.endswith(".pkl") ]
for f in filelist:
    os.remove(os.path.join(dir, f))

serialize(IcmpRouteVerifier(), os.path.join(dir, 'icmpRouteVerifier.pkl'))
serialize(HttpHandler(), os.path.join(dir, 'httpHandler.pkl'))
serialize(FonaRaspberryPiHandler(), os.path.join(dir, 'fonaRaspberryPiHandler.pkl'))
serialize(LogHandler(), os.path.join(dir, 'logHandler.pkl'))
